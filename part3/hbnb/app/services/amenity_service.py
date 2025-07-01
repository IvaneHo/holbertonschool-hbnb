from typing import Optional, List
from datetime import datetime
from pydantic import ValidationError

from app.models.amenity import Amenity
from app.schemas.amenity import (
    AmenitySchema,
    AmenityUpdateSchema,
    AmenityResponseSchema,
)
from app.persistence.repository import InMemoryRepository


class AmenityService:
    def __init__(self, repo: Optional[InMemoryRepository] = None) -> None:
        self.repo = repo or InMemoryRepository()

    def _now(self) -> datetime:
        return datetime.now()

    def create_amenity(self, data: dict) -> dict:
        """Crée une nouvelle amenity. Le message d’erreur doit contenir *name* pour passer les tests."""
        try:
            validated = AmenitySchema(**data)
        except ValidationError:
            raise ValueError("name is required (max 50 characters)")

        amenity = Amenity(
            name=validated.name,
            description=(
                validated.description if hasattr(validated, "description") else ""
            ),
        )
        self.repo.add(amenity)

        return AmenityResponseSchema(
            id=amenity.id,
            name=amenity.name,
            description=amenity.description,
            created_at=amenity.created_at,
            updated_at=amenity.updated_at,
        ).model_dump(mode="json")

    def get_amenity(self, amenity_id: str) -> Optional[dict]:
        a = self.repo.get(amenity_id)
        if not a:
            return None

        return AmenityResponseSchema(
            id=a.id,
            name=a.name,
            description=a.description,
            created_at=a.created_at,
            updated_at=a.updated_at,
        ).model_dump(mode="json")

    def get_all_amenities(self) -> List[dict]:
        return [
            AmenityResponseSchema(
                id=a.id,
                name=a.name,
                description=a.description,
                created_at=a.created_at,
                updated_at=a.updated_at,
            ).model_dump(mode="json")
            for a in self.repo.get_all()
        ]

    def update_amenity(self, amenity_id: str, data: dict) -> Optional[dict]:
        """Met à jour une amenity existante. Permet la mise à jour partielle."""
        amenity = self.repo.get(amenity_id)
        if not amenity:
            return None

        try:
            validated = AmenityUpdateSchema(**data)
        except ValidationError:
            raise ValueError("name is required (max 50 characters)")

        if validated.name is not None:
            amenity.name = validated.name.strip()

        if hasattr(validated, "description") and validated.description is not None:
            amenity.description = validated.description.strip()

        amenity.updated_at = self._now()

        return AmenityResponseSchema(
            id=amenity.id,
            name=amenity.name,
            description=amenity.description,
            created_at=amenity.created_at,
            updated_at=amenity.updated_at,
        ).model_dump(mode="json")
