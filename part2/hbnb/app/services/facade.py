from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository
from app.schemas.user import UserResponseSchema
from app.schemas.place import PlaceResponseSchema
from pydantic import BaseModel, EmailStr, ValidationError


class EmailValidator(BaseModel):
    email: EmailStr


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # === USER LOGIC ===
    def _validate_email(self, email: str):
        try:
            EmailValidator(email=email)
        except ValidationError:
            raise ValueError("Invalid email format")
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

    # === PLACE LOGIC ===
    def _validate_place_data(self, data):
        if data['price'] < 0:
            raise ValueError("Price must be non-negative")
        if not (-90 <= data['latitude'] <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= data['longitude'] <= 180):
            raise ValueError("Longitude must be between -180 and 180")

    def create_place(self, place_data):
        self._validate_place_data(place_data)

        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        amenities = []
        for amenity_id in place_data['amenities']:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with id {amenity_id} not found")
            amenities.append(amenity)

        place = Place(**place_data)
        place.amenities = amenities
        self.place_repo.add(place)

        return PlaceResponseSchema.from_place(place).model_dump(mode="json")

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return PlaceResponseSchema.from_place(place).model_dump(mode="json")

    def get_all_places(self):
        result = []
        for p in self.place_repo.get_all():
            try:
                result.append(PlaceResponseSchema.from_place(p).model_dump(mode="json"))
            except ValidationError:
                continue
        return result

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        self._validate_place_data(place_data)

        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        amenities = []
        for amenity_id in place_data['amenities']:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with id {amenity_id} not found")
            amenities.append(amenity)

        place.title = place_data['title']
        place.description = place_data['description']
        place.price = place_data['price']
        place.latitude = place_data['latitude']
        place.longitude = place_data['longitude']
        place.owner_id = place_data['owner_id']
        place.amenities = amenities
        place.updated_at = self.place_repo._now()

        return PlaceResponseSchema.from_place(place).model_dump(mode="json")
