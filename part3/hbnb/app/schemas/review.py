from pydantic import BaseModel, Field
from typing import Annotated, Optional
from datetime import datetime

class ReviewSchema(BaseModel):
    text: Annotated[str, Field(min_length=1)]
    rating: Annotated[int, Field(ge=1, le=5)]
    user_id: str
    place_id: str

class ReviewUpdateSchema(BaseModel):
    text: Optional[Annotated[str, Field(min_length=1)]] = None
    rating: Optional[Annotated[int, Field(ge=1, le=5)]] = None

class ReviewResponseSchema(BaseModel):
    id: str
    text: str
    rating: int
    user_id: str
    place_id: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, review):
        """Crée une ReviewResponseSchema depuis un objet Review SQLAlchemy"""
        return cls(
            id=review.id,
            text=review.text,
            rating=review.rating,
            user_id=review.user_id,
            place_id=review.place_id,
            created_at=review.created_at,
            updated_at=review.updated_at,
        )

    class Config:
        from_attributes = True
