"""
Service layer (facade) centralise toute la logique métier HBnB.
"""

from typing import List, Optional

from app.services.user_service import UserService
from app.services.place_service import PlaceService
from app.services.amenity_service import AmenityService
from app.services.review_service import ReviewService
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository

from app.models.user import User      # SQLAlchemy
from app.models.place import PlaceORM # <-- ICI LE MODÈLE ORM
from app.models.amenity import Amenity, AmenityORM   
from app.models.review import Review

class HBnBFacade:
    """Couche d'accès unique aux services métier utilisée par les routes API."""

    def __init__(self):
        # Initialisation des repositories SQLAlchemy (ORM, pas métier)
        self.user_repo = UserRepository()                    # <-- Remplacé ici
        self.place_repo = SQLAlchemyRepository(PlaceORM)
        self.amenity_repo = SQLAlchemyRepository(AmenityORM)  
        self.review_repo = SQLAlchemyRepository(Review)

        # Initialisation des services avec leurs dépendances
        self.user_service = UserService(self.user_repo)
        self.place_service = PlaceService(
            self.place_repo, self.user_repo, self.amenity_repo
        )
        self.amenity_service = AmenityService(self.amenity_repo)
        self.review_service = ReviewService(
            self.review_repo, self.user_repo, self.place_repo
        )

    # ------------------------------ UTILISATEUR ----------------------------- #

    def create_user(self, data: dict) -> dict:
        return self.user_service.create_user(data)

    def get_user(self, user_id: str) -> Optional[dict]:
        return self.user_service.get_user(user_id)

    def get_all_users(self) -> List[dict]:
        return self.user_service.get_all_users()

    def update_user(self, user_id: str, data: dict) -> Optional[dict]:
        return self.user_service.update_user(user_id, data)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_service.get_user_by_email(email)

    # -------------------------------- PLACE -------------------------------- #

    def create_place(self, data: dict) -> dict:
        return self.place_service.create_place(data)

    def get_place(self, place_id: str) -> Optional[dict]:
        return self.place_service.get_place(place_id)

    def get_all_places(self) -> List[dict]:
        return self.place_service.get_all_places()

    def update_place(self, place_id: str, data: dict) -> Optional[dict]:
        return self.place_service.update_place(place_id, data)

    # -------------------------------- AMENITY ------------------------------ #

    def create_amenity(self, data: dict) -> dict:
        return self.amenity_service.create_amenity(data)

    def get_amenity(self, amenity_id: str) -> Optional[dict]:
        return self.amenity_service.get_amenity(amenity_id)

    def get_all_amenities(self) -> List[dict]:
        return self.amenity_service.get_all_amenities()

    def update_amenity(self, amenity_id: str, data: dict) -> Optional[dict]:
        return self.amenity_service.update_amenity(amenity_id, data)

    # -------------------------------- REVIEW ------------------------------- #

    def create_review(self, data: dict) -> dict:
        return self.review_service.create_review(data)

    def get_review(self, review_id: str) -> Optional[dict]:
        return self.review_service.get_review(review_id)

    def get_all_reviews(self) -> List[dict]:
        return self.review_service.get_all_reviews()

    def get_reviews_by_place(self, place_id: str) -> Optional[List[dict]]:
        return self.review_service.get_reviews_by_place(place_id)

    def update_review(self, review_id: str, data: dict) -> Optional[dict]:
        return self.review_service.update_review(review_id, data)

    def delete_review(self, review_id: str) -> Optional[dict]:
        return self.review_service.delete_review(review_id)

# Instance globale utilisée par les routes
facade = HBnBFacade()
