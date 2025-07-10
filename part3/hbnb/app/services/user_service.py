from typing import List, Optional
from pydantic import BaseModel, EmailStr, ValidationError

from app.models.user import User
from app.schemas.user import UserResponseSchema, UserUpdateSchema
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

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
        # TOUJOURS normaliser l'email
        return self.repo.get_by_attribute("email", email.strip().lower())

    def create_user(self, data: dict) -> dict:
        email = data["email"].strip().lower()
        self._validate_email(email)
        if self.get_user_by_email(email):
            raise ValueError("email already registered")

        password = data.get("password")
        if not password or not isinstance(password, str) or len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

        user_data = data.copy()
        user_data["email"] = email  # normalisé
        user_data["password"] = password  # <-- PAS de hash ici, hash fait dans User
        user = User(**user_data)
        self.repo.add(user)
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

        if "email" in validated_data:
            email = validated_data["email"].strip().lower()
            self._validate_email(email)
            existing_user = self.get_user_by_email(email)
            if existing_user and str(existing_user.id) != str(user_id):
                raise ValueError("email already registered")
            validated_data["email"] = email

        for field, value in validated_data.items():
            if field == "password":
                if not isinstance(value, str) or len(value) < 8:
                    raise ValueError("Password must be at least 8 characters")
                user.hash_password(value)   
            else:
                setattr(user, field, value)

        from app import db
        db.session.commit()
        return UserResponseSchema.model_validate(user).model_dump(mode="json")
