from pydantic import BaseModel, constr # type: ignore
from datetime import datetime

class AmenitySchema(BaseModel):
    name: constr(strip_whitespace=True, max_length=50) # type: ignore

class AmenityResponseSchema(AmenitySchema):
    id: str
    created_at: datetime
    updated_at: datetime
