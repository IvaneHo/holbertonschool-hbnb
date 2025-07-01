from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class AmenitySchema(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = Field(default="", max_length=255)

    @validator("name")
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("name is required (max 50 characters)")
        return v

    class Config:
        extra = "forbid"


class AmenityUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=255)

    @validator("name")
    def name_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("name must not be empty")
        return v

    class Config:
        extra = "forbid"


class AmenityResponseSchema(AmenitySchema):
    id: str
    created_at: datetime
    updated_at: datetime
