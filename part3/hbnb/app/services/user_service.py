from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ValidationError

from app.models.user import User
from app.schemas.user import UserResponseSchema, UserUpdateSchema
from app.persistence.repository import InMemoryRepository


class _EmailValidator(BaseModel):
    email: EmailStr


class UserService:
    def __init__(self, user_repo: InMemoryRepository):
        self.repo = user_repo

    def _now(self) -> datetime:
        return datetime.now()

    def _validate_email(self, email: str) -> None:
        try:
            _EmailValidator(email=email)
        except ValidationError:
            raise ValueError("invalid email format")

        if "." not in email.split("@")[-1]:
            raise ValueError("invalid email format")

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.repo.get_by_attribute("email", email)

    def create_user(self, data: dict) -> dict:
        self._validate_email(data["email"])
        if self.get_user_by_email(data["email"]):
            raise ValueError("email already registered")

        user = User(**data)
        self.repo.add(user)
        return UserResponseSchema.model_validate(user).model_dump(mode="json")

    def get_user(self, user_id: str) -> Optional[dict]:
        user = self.repo.get(user_id)
        if not user:
            return None
        return UserResponseSchema.model_validate(user).model_dump(mode="json")

    def get_all_users(self) -> List[dict]:
        res = []
        for user in self.repo.get_all():
            try:
                res.append(
                    UserResponseSchema.model_validate(user).model_dump(mode="json")
                )
            except ValidationError:
                continue
        return res

    def update_user(self, user_id: str, payload: dict) -> Optional[dict]:
        user = self.repo.get(user_id)
        if not user:
            return None

        # ✅ Validation partielle via Pydantic
        try:
            validated_data = UserUpdateSchema(**payload).model_dump(exclude_unset=True)
        except ValidationError as e:
            raise ValueError(e.errors()[0]["msg"])

        # Vérification de l'email si modifié
        if "email" in validated_data:
            self._validate_email(validated_data["email"])
            existing_user = self.get_user_by_email(validated_data["email"])
            if existing_user and existing_user.id != user_id:
                raise ValueError("email already registered")

        # Mise à jour des champs autorisés
        for field, value in validated_data.items():
            setattr(user, field, value)

        user.updated_at = self._now()
        return UserResponseSchema.model_validate(user).model_dump(mode="json")
