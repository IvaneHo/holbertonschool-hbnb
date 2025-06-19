"""
Service layer (facade)  centralise toute la logique métier HBnB.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, ValidationError

from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

from app.persistence.repository import InMemoryRepository

from app.schemas.user import UserResponseSchema
from app.schemas.place import PlaceResponseSchema
from app.schemas.review import ReviewResponseSchema
from app.schemas.amenity import AmenitySchema, AmenityResponseSchema


# --------------------------------------------------------------------------- #
#                 Validateurs ponctuels pour e-mail et Review                 #
# --------------------------------------------------------------------------- #
class _EmailValidator(BaseModel):
    email: EmailStr


class _ReviewValidator(BaseModel):
    text: str
    rating: int


# --------------------------------------------------------------------------- #
#                                   FACADE                                    #
# --------------------------------------------------------------------------- #
class HBnBFacade:
    """Couche métier unique pour l’API – évite la logique dans les routes."""

    def __init__(self) -> None:
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ----------------------------- UTILITAIRES ----------------------------- #
    @staticmethod
    def _now() -> datetime:
        return datetime.now()

    def _validate_email(self, email: str) -> None:
        """Vérifie la syntaxe d’un e-mail et la présence du '.' de domaine."""
        try:
            _EmailValidator(email=email)
        except ValidationError:
            raise ValueError("invalid email format")
        if "." not in email.split("@")[-1]:
            raise ValueError("invalid email format")

    # ------------------------------ UTILISATEUR ----------------------------- #
    def create_user(self, data: dict) -> dict:
        self._validate_email(data["email"])
        if self.get_user_by_email(data["email"]):
            raise ValueError("email already registered")

        user = User(**data)
        self.user_repo.add(user)
        return UserResponseSchema(**user.__dict__).model_dump(mode="json")

    def get_user(self, user_id: str) -> Optional[dict]:
        user = self.user_repo.get(user_id)
        if not user:
            return None
        return UserResponseSchema(**user.__dict__).model_dump(mode="json")

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self) -> List[dict]:
        res = []
        for u in self.user_repo.get_all():
            try:
                res.append(UserResponseSchema(**u.__dict__).model_dump(mode="json"))
            except ValidationError:
                continue
        return res

    def update_user(self, user_id: str, payload: dict) -> Optional[dict]:
        user = self.user_repo.get(user_id)
        if not user:
            return None

        if "email" in payload:
            self._validate_email(payload["email"])
            other = self.get_user_by_email(payload["email"])
            if other and other.id != user_id:
                raise ValueError("email already registered")
            user.email = payload["email"]

        if "first_name" in payload:
            user.first_name = payload["first_name"]
        if "last_name" in payload:
            user.last_name = payload["last_name"]

        user.updated_at = self._now()
        return UserResponseSchema(**user.__dict__).model_dump(mode="json")

    # -------------------------------- PLACE -------------------------------- #
    @staticmethod
    def _validate_place(data: dict) -> None:
        if data["price"] < 0:
            raise ValueError("price must be non-negative")
        if not (-90 <= data["latitude"] <= 90):
            raise ValueError("latitude must be between -90 and 90")
        if not (-180 <= data["longitude"] <= 180):
            raise ValueError("longitude must be between -180 and 180")

    def create_place(self, data: dict) -> dict:
        self._validate_place(data)

        owner = self.user_repo.get(data["owner_id"])
        if not owner:
            raise ValueError("owner not found")

        place = Place(
            title=data["title"],
            description=data.get("description", ""),
            price=data["price"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            owner=owner,
        )

        # Récupération/validation des amenities fournis
        amenity_objs: List[Amenity] = []
        for amenity_id in data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"amenity {amenity_id} not found")
            amenity_objs.append(amenity)
        place.amenities = amenity_objs

        self.place_repo.add(place)
        return PlaceResponseSchema.from_place(place).model_dump(mode="json")

    def get_place(self, place_id: str) -> Optional[dict]:
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return PlaceResponseSchema.from_place(place).model_dump(mode="json")

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

        self._validate_place(data)
        owner = self.user_repo.get(data["owner_id"])
        if not owner:
            raise ValueError("owner not found")

        place.title = data["title"]
        place.description = data.get("description", "")
        place.price = data["price"]
        place.latitude = data["latitude"]
        place.longitude = data["longitude"]
        place.owner = owner

        # amenities
        new_amenities: List[Amenity] = []
        for amenity_id in data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"amenity {amenity_id} not found")
            new_amenities.append(amenity)
        place.amenities = new_amenities

        place.updated_at = self._now()
        return PlaceResponseSchema.from_place(place).model_dump(mode="json")

    # -------------------------------- REVIEW ------------------------------- #
    def _serialize_review(self, r: Review) -> dict:
        return ReviewResponseSchema(
            id=r.id,
            text=r.text,
            rating=r.rating,
            user_id=r.user_id,
            place_id=r.place_id,
            created_at=r.created_at,
            updated_at=r.updated_at,
        ).model_dump(mode="json")

    def create_review(self, data: dict) -> dict:
        try:
            _ReviewValidator(**data)
        except ValidationError:
            raise ValueError("invalid review input data")

        if not (1 <= data["rating"] <= 5):
            raise ValueError("rating must be between 1 and 5")

        user = self.user_repo.get(data["user_id"])
        if not user:
            raise ValueError("user not found")

        place = self.place_repo.get(data["place_id"])
        if not place:
            raise ValueError("place not found")

        review = Review(
            text=data["text"],
            rating=data["rating"],
            user=user,
            place=place,
        )
        self.review_repo.add(review)
        return self._serialize_review(review)

    def get_review(self, review_id: str) -> Optional[dict]:
        r = self.review_repo.get(review_id)
        return None if not r else self._serialize_review(r)

    def get_all_reviews(self) -> List[dict]:
        return [self._serialize_review(r) for r in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id: str) -> Optional[List[dict]]:
        if not self.place_repo.get(place_id):
            return None
        return [self._serialize_review(r) for r in self.review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id: str, data: dict) -> Optional[dict]:
        r = self.review_repo.get(review_id)
        if not r:
            return None
        if "text" in data:
            r.text = data["text"]
        if "rating" in data:
            if not (1 <= data["rating"] <= 5):
                raise ValueError("rating must be between 1 and 5")
            r.rating = data["rating"]
        r.updated_at = self._now()
        return {"message": "review updated successfully"}

    def delete_review(self, review_id: str) -> Optional[dict]:
        if not self.review_repo.get(review_id):
            return None
        self.review_repo.delete(review_id)
        return {"message": "review deleted successfully"}

    # -------------------------------- AMENITY ------------------------------ #
    def create_amenity(self, data: dict) -> dict:
        """Crée un amenity – message d’erreur doit contenir *name* pour les tests."""
        try:
            validated = AmenitySchema(**data)
        except ValidationError:
            raise ValueError("name is required (max 50 characters)")

        amenity = Amenity(name=validated.name)
        self.amenity_repo.add(amenity)
        return AmenityResponseSchema(
            id=amenity.id,
            name=amenity.name,
            created_at=amenity.created_at,
            updated_at=amenity.updated_at,
        ).model_dump(mode="json")

    def get_amenity(self, amenity_id: str) -> Optional[dict]:
        a = self.amenity_repo.get(amenity_id)
        return None if not a else AmenityResponseSchema(
            id=a.id,
            name=a.name,
            created_at=a.created_at,
            updated_at=a.updated_at,
        ).model_dump(mode="json")

    def get_all_amenities(self) -> List[dict]:
        return [
            AmenityResponseSchema(
                id=a.id,
                name=a.name,
                created_at=a.created_at,
                updated_at=a.updated_at,
            ).model_dump(mode="json")
            for a in self.amenity_repo.get_all()
        ]

    def update_amenity(self, amenity_id: str, data: dict) -> Optional[dict]:
        """Met à jour un amenity existant avec validation."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        # Vérifie que le champ name est bien présent et non vide
        name = data.get("name")
        if not name or not name.strip():
            raise ValueError("name is required (max 50 characters)")

        try:
            validated = AmenitySchema(**data)
        except ValidationError:
            raise ValueError("name is required (max 50 characters)")

        amenity.name = validated.name
        amenity.updated_at = self._now()

        return AmenityResponseSchema(
            id=amenity.id,
            name=amenity.name,
            created_at=amenity.created_at,
            updated_at=amenity.updated_at,
        ).model_dump(mode="json")


