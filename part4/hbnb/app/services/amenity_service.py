from typing import Optional, List
from datetime import datetime, timezone
from pydantic import ValidationError
from app.models.amenity import Amenity


from app.schemas.amenity import (
    AmenitySchema,
    AmenityUpdateSchema,
    AmenityResponseSchema,
)

class AmenityService:
    def __init__(self, repo):
        self.repo = repo

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def create_amenity(self, data: dict) -> dict:
        try:
            validated = AmenitySchema(**data)
        except ValidationError:
            raise ValueError("name is required (max 50 characters)")

        amenity = Amenity(
            name=validated.name,
            description=getattr(validated, "description", "")
        )
        self.repo.add(amenity)
        if hasattr(self.repo, "commit"):
            self.repo.commit()
        # Ajout : recharge l'objet depuis la BDD si possible (pour avoir created_at/updated_at à jour)
        if hasattr(self.repo, "refresh"):
            self.repo.refresh(amenity)
        
        return AmenityResponseSchema(
            id=amenity.id,
            name=amenity.name,
            description=amenity.description,
            created_at=amenity.created_at or self._now(),
            updated_at=amenity.updated_at or self._now(),
        ).model_dump(mode="json")

    def get_amenity(self, amenity_id: str) -> Optional[dict]:
        a = self.repo.get(amenity_id)
        if not a:
            return None
        return AmenityResponseSchema(
            id=a.id,
            name=a.name,
            description=a.description,
            created_at=a.created_at or self._now(),
            updated_at=a.updated_at or self._now(),
        ).model_dump(mode="json")

    def get_all_amenities(self) -> List[dict]:
        return [
            AmenityResponseSchema(
                id=a.id,
                name=a.name,
                description=a.description,
                created_at=a.created_at or self._now(),
                updated_at=a.updated_at or self._now(),
            ).model_dump(mode="json")
            for a in self.repo.get_all()
        ]

    def update_amenity(self, amenity_id: str, data: dict) -> Optional[dict]:
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

        self.repo.update(amenity_id, data)
        if hasattr(self.repo, "commit"):
            self.repo.commit()
        if hasattr(self.repo, "refresh"):
            self.repo.refresh(amenity)
        return AmenityResponseSchema(
            id=amenity.id,
            name=amenity.name,
            description=amenity.description,
            created_at=amenity.created_at or self._now(),
            updated_at=amenity.updated_at or self._now(),
        ).model_dump(mode="json")

    def delete_amenity(self, amenity_id):
        return self.repo.delete(amenity_id)