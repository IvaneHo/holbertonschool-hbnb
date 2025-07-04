from datetime import datetime
from typing import List, Optional

from pydantic import ValidationError

from app.models.place import PlaceORM
from app.models.amenity import Amenity
from app.models.user import User
from app.schemas.place import PlaceResponseSchema, PlaceUpdateSchema, PlaceSchema
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class PlaceService:
    def __init__(
        self,
        place_repo: Optional[SQLAlchemyRepository] = None,
        user_repo: Optional[SQLAlchemyRepository] = None,
        amenity_repo: Optional[SQLAlchemyRepository] = None,
    ):
        self.place_repo = place_repo or SQLAlchemyRepository(PlaceORM)
        self.user_repo = user_repo or SQLAlchemyRepository(User)
        self.amenity_repo = amenity_repo or SQLAlchemyRepository(Amenity)

    def _now(self):
        return datetime.now()

    def _validate_coords(self, lat: float, lon: float):
        if not (-90 <= lat <= 90):
            raise ValueError("latitude must be between -90 and 90")
        if not (-180 <= lon <= 180):
            raise ValueError("longitude must be between -180 and 180")

    def create_place(self, data: dict) -> dict:
        # On suppose que data est déjà validé par Pydantic côté API (PlaceSchema)
        # On vérifie l'owner
        owner_id = data.get("owner_id")
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("owner not found")

        self._validate_coords(data["latitude"], data["longitude"])
        if data["price"] < 0:
            raise ValueError("price must be non-negative")

        # On ne gère pas encore la jointure amenities <-> place en ORM (à ajouter si tu veux)
        place = PlaceORM(
            title=data["title"],
            description=data.get("description", ""),
            price=data["price"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            owner_id=owner_id,
        )

        self.place_repo.add(place)

        # Tu peux charger les amenities en extra si tu veux, pour l’API (pas persisté ici)
        amenities_names = []
        for a_id in data.get("amenities", []):
            amenity = self.amenity_repo.get(a_id)
            if amenity:
                amenities_names.append(amenity.name)

        # Création du schéma Pydantic pour la sortie
        return PlaceResponseSchema(
            id=place.id,
            title=place.title,
            description=place.description,
            price=place.price,
            latitude=place.latitude,
            longitude=place.longitude,
            owner_id=place.owner_id,
            amenities=amenities_names,
            created_at=str(place.created_at) if hasattr(place, "created_at") else "",
            updated_at=str(place.updated_at) if hasattr(place, "updated_at") else "",
        ).model_dump(mode="json")

    def get_place(self, place_id: str) -> Optional[dict]:
        place = self.place_repo.get(place_id)
        if not place:
            return None
        # Ici tu charges aussi les amenities si besoin
        return PlaceResponseSchema(
            id=place.id,
            title=place.title,
            description=place.description,
            price=place.price,
            latitude=place.latitude,
            longitude=place.longitude,
            owner_id=place.owner_id,
            amenities=[],  # À implémenter : jointure many-to-many SQLAlchemy
            created_at=str(place.created_at) if hasattr(place, "created_at") else "",
            updated_at=str(place.updated_at) if hasattr(place, "updated_at") else "",
        ).model_dump(mode="json")

    def get_all_places(self) -> List[dict]:
        res = []
        for place in self.place_repo.get_all():
            try:
                res.append(
                    PlaceResponseSchema(
                        id=place.id,
                        title=place.title,
                        description=place.description,
                        price=place.price,
                        latitude=place.latitude,
                        longitude=place.longitude,
                        owner_id=place.owner_id,
                        amenities=[],  # Idem ci-dessus
                        created_at=str(place.created_at) if hasattr(place, "created_at") else "",
                        updated_at=str(place.updated_at) if hasattr(place, "updated_at") else "",
                    ).model_dump(mode="json")
                )
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

        # amenities à gérer côté SQLAlchemy si tu as une association

        self.place_repo.update(place_id, data)
        # Recharge le place après update
        place = self.place_repo.get(place_id)
        return PlaceResponseSchema(
            id=place.id,
            title=place.title,
            description=place.description,
            price=place.price,
            latitude=place.latitude,
            longitude=place.longitude,
            owner_id=place.owner_id,
            amenities=[],  # Idem
            created_at=str(place.created_at) if hasattr(place, "created_at") else "",
            updated_at=str(place.updated_at) if hasattr(place, "updated_at") else "",
        ).model_dump(mode="json")
