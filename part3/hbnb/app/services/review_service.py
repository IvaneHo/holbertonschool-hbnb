from datetime import datetime
from typing import Optional, List
from pydantic import ValidationError

from app.models.review import Review
from app.models.place import Place
from app.models.user import User
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.schemas.review import ReviewResponseSchema

from pydantic import BaseModel, Field


class _ReviewValidator(BaseModel):
    text: str = Field(..., min_length=1)
    rating: int = Field(..., ge=1, le=5)
    user_id: str
    place_id: str


class ReviewService:
    def __init__(self, review_repo, user_repo, place_repo):
        self.review_repo = review_repo
        self.user_repo = user_repo
        self.place_repo = place_repo

    def _now(self):
        return datetime.now()

    def _serialize(self, review):
        return ReviewResponseSchema(
            id=review.id,
            text=review.text,
            rating=review.rating,
            user_id=review.user_id,
            place_id=review.place_id,
            created_at=review.created_at,
            updated_at=review.updated_at,
        ).model_dump(mode="json")

    def create_review(self, data):
        try:
            validated = _ReviewValidator(**data)
        except ValidationError:
            raise ValueError("invalid review input data")

        user = self.user_repo.get(validated.user_id)
        place = self.place_repo.get(validated.place_id)
        if not user:
            raise ValueError("user not found")
        if not place:
            raise ValueError("place not found")

        # --- Règle 1 : pas le droit de reviewer son propre lieu
        # ATTENTION : adapte selon ta structure Place (ici owner_id attendu !)
        owner_id = getattr(place, "owner_id", None)
        if not owner_id and hasattr(place, "owner") and hasattr(place.owner, "id"):
            owner_id = place.owner.id
        if owner_id == validated.user_id:
            raise ValueError("You cannot review your own place")

        # --- Règle 2 : pas deux reviews pour le même lieu/user
        for review in self.review_repo.get_all():
            if (
                review.user_id == validated.user_id
                and review.place_id == validated.place_id
            ):
                raise ValueError("You have already reviewed this place")

        review = Review(
            text=validated.text,
            rating=validated.rating,
            user_id=validated.user_id,    # <-- la clé étrangère
            place_id=validated.place_id,
        )
        self.review_repo.add(review)
        return self._serialize(review)

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        # PATCH ICI : si review est None ou a un id None (donc "faux" objet après delete)
        if not review or not getattr(review, "id", None):
            return None
        return self._serialize(review)

    def get_all_reviews(self):
        return [self._serialize(r) for r in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id):
        if not self.place_repo.get(place_id):
            raise ValueError("place not found")
        return [
            self._serialize(r)
            for r in self.review_repo.get_all()
            if r.place_id == place_id
        ]

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if "text" in data:
            review.text = data["text"]
        if "rating" in data:
            rating = data["rating"]
            if not (1 <= rating <= 5):
                raise ValueError("rating must be between 1 and 5")
            review.rating = rating

        review.updated_at = self._now()
        return self._serialize(review)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return {"message": "review deleted successfully"}
