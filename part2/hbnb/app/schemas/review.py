from pydantic import BaseModel, conint # type: ignore
from datetime import datetime

class ReviewSchema(BaseModel):
    text: str
    rating: conint(ge=1, le=5) # type: ignore
    place_id: str
    user_id: str

class ReviewResponseSchema(ReviewSchema):
    id: str
    created_at: datetime
    updated_at: datetime
