from pydantic import BaseModel, EmailStr, ValidationError
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.schemas.amenity import AmenityResponseSchema
from app.models.review import Review
from app.persistence.repository import InMemoryRepository
from app.schemas.user import UserResponseSchema
from app.schemas.place import PlaceResponseSchema
from app.schemas.review import ReviewResponseSchema

class EmailValidator(BaseModel):
    email: EmailStr

class ReviewValidator(BaseModel):
    text: str
    rating: int

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

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

        if 'email' in updated_data:
            self._validate_email(updated_data['email'])
            existing = self.get_user_by_email(updated_data['email'])
            if existing and existing.id != user_id:
                raise ValueError("Email already registered by another user")
            user.email = updated_data['email']

        if 'first_name' in updated_data:
            user.first_name = updated_data['first_name']

        if 'last_name' in updated_data:
            user.last_name = updated_data['last_name']

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
        for amenity_id in place_data.get('amenities', []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with id {amenity_id} not found")
            amenities.append(amenity)

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ""),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )
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
        for amenity_id in place_data.get('amenities', []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with id {amenity_id} not found")
            amenities.append(amenity)

        place.title = place_data['title']
        place.description = place_data['description']
        place.price = place_data['price']
        place.latitude = place_data['latitude']
        place.longitude = place_data['longitude']
        place.owner = owner
        place.amenities = amenities
        place.updated_at = self.place_repo._now()

        return PlaceResponseSchema.from_place(place).model_dump(mode="json")

    # === REVIEW LOGIC ===
    def _serialize_review(self, review):
        return ReviewResponseSchema(
            id=review.id,
            text=review.text,
            rating=review.rating,
            user_id=review.user_id,
            place_id=review.place_id,
            created_at=review.created_at,
            updated_at=review.updated_at
        ).model_dump(mode="json")

    def create_review(self, review_data):
        try:
            ReviewValidator(**review_data)
        except ValidationError:
            raise ValueError("Invalid review input data")

        if not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5")

        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place
        )
        self.review_repo.add(review)
        return self._serialize_review(review)

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        return self._serialize_review(review)

    def get_all_reviews(self):
        result = []
        for r in self.review_repo.get_all():
            try:
                result.append(self._serialize_review(r))
            except ValidationError:
                continue
        return result

    def get_reviews_by_place(self, place_id):
        if not self.place_repo.get(place_id):
            return None
        result = []
        for r in self.review_repo.get_all():
            if r.place_id == place_id:
                try:
                    result.append(self._serialize_review(r))
                except ValidationError:
                    continue
        return result

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if 'text' in review_data:
            review.text = review_data['text']

        if 'rating' in review_data:
            if not (1 <= review_data['rating'] <= 5):
                raise ValueError("Rating must be between 1 and 5")
            review.rating = review_data['rating']

        review.updated_at = self.review_repo._now()
        return {"message": "Review updated successfully"}

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}

    # === AMENITY LOGIC ===
    def create_amenity(self, amenity_data):
        if 'name' not in amenity_data or not amenity_data['name'].strip():
            raise ValueError("Amenity 'name' is required.")
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

   
def update_amenity(self, amenity_id, amenity_data):
    amenity = self.amenity_repo.get(amenity_id)
    if not amenity:
        return None

    if 'name' in amenity_data:
        if not amenity_data['name'].strip():
            raise ValueError("Amenity 'name' cannot be empty.")
        amenity.name = amenity_data['name']

    amenity.updated_at = self.amenity_repo._now()
    return AmenityResponseSchema(
        id=amenity.id,
        name=amenity.name,
        created_at=amenity.created_at,
        updated_at=amenity.updated_at
    ).model_dump(mode="json")
