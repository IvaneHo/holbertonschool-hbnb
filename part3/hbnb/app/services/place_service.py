from datetime import datetime
from typing import List, Optional

from pydantic import ValidationError

from app.models.place import Place
from app.models.amenity import Amenity
from app.models.user import User
from app.schemas.place import PlaceResponseSchema, PlaceUpdateSchema
from app.persistence.repository import InMemoryRepository


class PlaceService:
    def __init__(
        self,
        place_repo: Optional[InMemoryRepository] = None,
        user_repo: Optional[InMemoryRepository] = None,
        amenity_repo: Optional[InMemoryRepository] = None,
    ):
        self.place_repo = place_repo or InMemoryRepository()
        self.user_repo = user_repo or InMemoryRepository()
        self.amenity_repo = amenity_repo or InMemoryRepository()

    def _now(self):
        return datetime.now()

    def _validate_coords(self, lat: float, lon: float):
        if not (-90 <= lat <= 90):
            raise ValueError("latitude must be between -90 and 90")
        if not (-180 <= lon <= 180):
            raise ValueError("longitude must be between -180 and 180")

    def create_place(self, data: dict) -> dict:
        owner = self.user_repo.get(data.get("owner_id"))
        if not owner:
            raise ValueError("owner not found")

        self._validate_coords(data["latitude"], data["longitude"])
        if data["price"] < 0:
            raise ValueError("price must be non-negative")

        amenities: List[Amenity] = []
        for a_id in data.get("amenities", []):
            amenity = self.amenity_repo.get(a_id)
            if not amenity:
                raise ValueError(f"amenity {a_id} not found")
            amenities.append(amenity)

        place = Place(
            title=data["title"],
            description=data.get("description", ""),
            price=data["price"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            owner=owner,
            amenities=amenities,
        )

        self.place_repo.add(place)
        return PlaceResponseSchema.from_place(place).model_dump(mode="json")

    def get_place(self, place_id: str) -> Optional[dict]:
        place = self.place_repo.get(place_id)
        return (
            None
            if not place
            else PlaceResponseSchema.from_place(place).model_dump(mode="json")
        )

    def get_all_places(self) -> List[dict]:
        res = []
        for p in self.place_repo.get_all():
            try:
                res.append(PlaceResponseSchema.from_place(p).model_dump(mode="json"))
            except ValidationError:
                continue
        return res

    def update_place(self, place_id: str, data: dict) -> Optional[dict]:
        place = self.place_repo.get(place_id)
        if not place:
            return None

        try:
            validated = PlaceUpdateSchema(**data)
        except ValidationError:
            raise ValueError("Invalid update data")

        if validated.owner_id:
            owner = self.user_repo.get(validated.owner_id)
            if not owner:
                raise ValueError("owner not found")
            place.owner = owner

        if validated.latitude is not None:
            self._validate_coords(validated.latitude, place.longitude)
            place.latitude = validated.latitude

        if validated.longitude is not None:
            self._validate_coords(place.latitude, validated.longitude)
            place.longitude = validated.longitude

        if validated.price is not None:
            if validated.price < 0:
                raise ValueError("price must be non-negative")
            place.price = validated.price

        if validated.title is not None:
            place.title = validated.title.strip()

        if validated.description is not None:
            place.description = validated.description.strip()

        if validated.amenities is not None:
            new_amenities: List[Amenity] = []
            for a_id in validated.amenities:
                amenity = self.amenity_repo.get(a_id)
                if not amenity:
                    raise ValueError(f"amenity {a_id} not found")
                new_amenities.append(amenity)
            place.amenities = new_amenities

        place.updated_at = self._now()

        return PlaceResponseSchema.from_place(place).model_dump(mode="json")
