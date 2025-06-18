from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime


class ReviewSchema(BaseModel):
    text: str
    rating: Annotated[int, Field(ge=1, le=5)]
    user_id: str
    place_id: str


class ReviewResponseSchema(ReviewSchema):
    id: str
    created_at: datetime
    updated_at: datetime
