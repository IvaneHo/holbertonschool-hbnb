from typing import List, Optional
from pydantic import BaseModel, EmailStr, ValidationError
from argon2 import PasswordHasher

from app.models.user import User
from app.schemas.user import UserResponseSchema, UserUpdateSchema
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

# Liste des domaines email jetables interdits 
BANNED_DOMAINS = {
    "mailinator.com",
    "10minutemail.com",
    "tempmail.com",
    "guerrillamail.com",
    "yopmail.com",
    "dispostable.com",
}

class _EmailValidator(BaseModel):
    email: EmailStr

class UserService:
    def __init__(self, user_repo: SQLAlchemyRepository):
        self.repo = user_repo
        self.hasher = PasswordHasher()

    def _validate_email(self, email: str) -> None:
        try:
            _EmailValidator(email=email)
        except ValidationError:
            raise ValueError("invalid email format")
        domain = email.split("@")[-1].lower()
        if "." not in domain:
            raise ValueError("invalid email format (no dot in domain)")
        if domain in BANNED_DOMAINS:
            raise ValueError(f"Domaine email interdit : {domain}")

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.repo.get_by_attribute("email", email)

    def create_user(self, data: dict) -> dict:
        self._validate_email(data["email"])
        if self.get_user_by_email(data["email"]):
            raise ValueError("email already registered")

        password = data.get("password")
        if not password or not isinstance(password, str) or len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

        # On hash le password avant stockage
        user_data = data.copy()
        user_data["password"] = self.hasher.hash(password)
        user = User(**user_data)
        self.repo.add(user)
        # commit explicite pour SQLAlchemy
        from app import db
        db.session.commit()
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

        try:
            validated_data = UserUpdateSchema(**payload).model_dump(exclude_unset=True)
        except ValidationError as e:
            raise ValueError(e.errors()[0]["msg"])

        # Vérifie email si modifié
        if "email" in validated_data:
            self._validate_email(validated_data["email"])
            existing_user = self.get_user_by_email(validated_data["email"])
            if existing_user and str(existing_user.id) != str(user_id):
                raise ValueError("email already registered")

        for field, value in validated_data.items():
            if field == "password":
                # Hash du nouveau password si modifié
                if not isinstance(value, str) or len(value) < 8:
                    raise ValueError("Password must be at least 8 characters")
                setattr(user, "password", self.hasher.hash(value))
            else:
                setattr(user, field, value)

        from app import db
        db.session.commit()
        return UserResponseSchema.model_validate(user).model_dump(mode="json")
