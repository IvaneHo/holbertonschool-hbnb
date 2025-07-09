"""
Service layer (facade) centralise toute la logique métier HBnB.
"""

from typing import List, Optional

from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    """Couche d'accès unique aux services métier utilisée par les routes API."""

    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ------------------------------ UTILISATEUR ----------------------------- #

    def create_user(self, data: dict) -> User:
        user = User(**data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_repo.get(user_id)

    def get_all_users(self) -> List[User]:
        return self.user_repo.get_all()

    def update_user(self, user_id: str, data: dict) -> Optional[User]:
        return self.user_repo.update(user_id, data)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repo.get_by_attribute("email", email)

    # -------------------------------- PLACE -------------------------------- #

    def create_place(self, data: dict) -> Place:
        place = Place(**data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id: str) -> Optional[Place]:
        return self.place_repo.get(place_id)

    def get_all_places(self) -> List[Place]:
        return self.place_repo.get_all()

    def update_place(self, place_id: str, data: dict) -> Optional[Place]:
        return self.place_repo.update(place_id, data)

    def delete_place(self, place_id: str):
        return self.place_repo.delete(place_id)

    # -------------------------------- AMENITY ------------------------------ #

    def create_amenity(self, data: dict) -> Amenity:
        amenity = Amenity(**data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self) -> List[Amenity]:
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id: str, data: dict) -> Optional[Amenity]:
        return self.amenity_repo.update(amenity_id, data)

    def delete_amenity(self, amenity_id: str):
        return self.amenity_repo.delete(amenity_id)

    # -------------------------------- REVIEW ------------------------------- #

    def create_review(self, data: dict) -> Review:
        review = Review(**data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id: str) -> Optional[Review]:
        return self.review_repo.get(review_id)

    def get_all_reviews(self) -> List[Review]:
        return self.review_repo.get_all()

    def update_review(self, review_id: str, data: dict) -> Optional[Review]:
        return self.review_repo.update(review_id, data)

    def delete_review(self, review_id: str):
        return self.review_repo.delete(review_id)

# Instance globale utilisée par les routes
facade = HBnBFacade()
