from app.models.user import User
from app.persistence.repository import InMemoryRepository
from app.schemas.user import UserResponseSchema
from pydantic import BaseModel, EmailStr, ValidationError


class EmailValidator(BaseModel):
    email: EmailStr


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def _validate_email(self, email: str):
        try:
            EmailValidator(email=email)  # Valide le format email
        except ValidationError:
            raise ValueError("Invalid email format")

        # Vérifie qu'il y a un point dans le domaine
        if '.' not in email.split('@')[-1]:
            raise ValueError("Email domain must contain a dot")

    def create_user(self, user_data):
        email = user_data['email']
        self._validate_email(email)

        if self.get_user_by_email(email):
            raise ValueError("Email already registered")

        user = User(**user_data)
        self.user_repo.add(user)

        return UserResponseSchema(**user.__dict__).model_dump(mode="json")

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        return UserResponseSchema(**user.__dict__).model_dump(mode="json")

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        result = []
        for u in self.user_repo.get_all():
            try:
                result.append(UserResponseSchema(**u.__dict__).model_dump(mode="json"))
            except ValidationError:
                continue
        return result

    def update_user(self, user_id, updated_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        new_email = updated_data['email']
        self._validate_email(new_email)

        existing = self.get_user_by_email(new_email)
        if existing and existing.id != user_id:
            raise ValueError("Email already registered by another user")

        user.first_name = updated_data['first_name']
        user.last_name = updated_data['last_name']
        user.email = new_email
        user.updated_at = self.user_repo._now()

        return UserResponseSchema(**user.__dict__).model_dump(mode="json")
