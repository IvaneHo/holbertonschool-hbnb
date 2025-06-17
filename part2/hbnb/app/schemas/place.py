from pydantic import BaseModel, condecimal, constr, conlist # type: ignore
from typing import Optional, List
from datetime import datetime

class PlaceSchema(BaseModel):
    title: constr(strip_whitespace=True, max_length=100) # type: ignore
    description: Optional[str] = ""
    price: condecimal(gt=0) # type: ignore
    latitude: float
    longitude: float
    owner_id: str  # id du user

class PlaceResponseSchema(PlaceSchema):
    id: str
    created_at: datetime
    updated_at: datetime
    amenities: List[str] = []
    reviews: List[str] = []
