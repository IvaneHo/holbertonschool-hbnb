"""
Service layer (facade) centralise toute la logique métier HBnB.
"""

from typing import List, Optional

from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.reservation_repository import ReservationRepository
from app.persistence.place_image_repository import PlaceImageRepository
 
  
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.place_image import PlaceImage

from app.services.place_service import PlaceService
from app.services.review_service import ReviewService
from app.services.amenity_service import AmenityService
from app.services.reservation_service import ReservationService

class HBnBFacade:
    """Couche d'accès unique aux services métier utilisée par les routes API."""

    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()
        self.reservation_repo = ReservationRepository()
        self.reservation_service = ReservationService()
        self.place_image_repo = PlaceImageRepository()
        
        
        self.place_service = PlaceService(self.place_repo, self.user_repo, self.amenity_repo , self.place_image_repo)
        self.amenity_service = AmenityService(self.amenity_repo)
        self.review_service = ReviewService(
            self.review_repo,
            self.user_repo,
            self.place_repo
        )

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

    def delete_user(self, user_id: str):
        return self.user_repo.delete(user_id)

    # -------------------------------- PLACE -------------------------------- #

    def create_place(self, data: dict) -> dict:
        return self.place_service.create_place(data)

    def get_place(self, place_id: str) -> Optional[dict]:
        return self.place_service.get_place(place_id)

    def get_all_places(self) -> List[dict]:
        return self.place_service.get_all_places()

    def update_place(self, place_id: str, data: dict) -> Optional[dict]:
        return self.place_service.update_place(place_id, data)

    def delete_place(self, place_id: str):
        return self.place_repo.delete(place_id)

    # -------------------------------- AMENITY ------------------------------ #

    def create_amenity(self, data: dict) -> dict:
        return self.amenity_service.create_amenity(data)

    def get_amenity(self, amenity_id: str) -> Optional[dict]:
        return self.amenity_service.get_amenity(amenity_id)

    def get_all_amenities(self) -> List[dict]:
        return self.amenity_service.get_all_amenities()

    def update_amenity(self, amenity_id: str, data: dict) -> Optional[dict]:
        return self.amenity_service.update_amenity(amenity_id, data)

    def delete_amenity(self, amenity_id: str):
        return self.amenity_service.delete_amenity(amenity_id)

    # -------------------------------- REVIEW ------------------------------- #

    def create_review(self, data: dict) -> dict:
        return self.review_service.create_review(data)

    def get_review(self, review_id: str) -> Optional[dict]:
        return self.review_service.get_review(review_id)

    def get_reviews_by_place(self, place_id: str) -> list:
        return self.review_service.get_reviews_by_place(place_id)

    def get_all_reviews(self) -> list:
        return self.review_service.get_all_reviews()

    def update_review(self, review_id: str, data: dict) -> Optional[dict]:
        return self.review_service.update_review(review_id, data)

    def delete_review(self, review_id: str):
        return self.review_service.delete_review(review_id)

    # ----------------------------- RESERVATION ------------------------------- #
    def create_reservation(self, user_id, data):
        return self.reservation_service.create_reservation(user_id, data)

    def get_reservation(self, res_id):
        return self.reservation_service.get_reservation(res_id)

    def get_all_reservations(self):
        return self.reservation_service.get_all_reservations()

    def update_reservation(self, res_id, data):
        return self.reservation_service.update_reservation(res_id, data)

    def delete_reservation(self, res_id):
        return self.reservation_service.delete_reservation(res_id)


# Instance globale utilisée par les routes
facade = HBnBFacade()
