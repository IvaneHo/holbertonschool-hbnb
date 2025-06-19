from pydantic import BaseModel, condecimal, constr, conlist # type: ignore
from typing import Optional, List
from datetime import datetime
from app.models.place import Place


class PlaceResponseSchema(BaseModel):
    id: str
    title: str
    description: str
    price: int
    latitude: float
    longitude: float
    owner_id: str
    amenities: List[str]
    created_at: str
    updated_at: str

    @classmethod
    def from_place(cls, place: Place) -> "PlaceResponseSchema":
        return cls(
            id=place.id,
            title=place.title,
            description=place.description,
            price=place.price,
            latitude=place.latitude,
            longitude=place.longitude,
            owner_id=place.owner.id,
            amenities=[a.id for a in place.amenities],
            created_at=str(place.created_at),
            updated_at=str(place.updated_at),
        )
