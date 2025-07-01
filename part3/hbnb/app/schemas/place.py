from pydantic import BaseModel, condecimal, constr, conlist  # type: ignore
from typing import Optional, List
from datetime import datetime
from app.models.place import Place


# Schéma utilisé pour créer un nouveau lieu (Place)
class PlaceSchema(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=100)  # type: ignore
    description: constr(strip_whitespace=True, max_length=255)  # type: ignore
    price: int
    latitude: float
    longitude: float
    owner_id: str
    amenities: List[str]

    class Config:
        extra = "forbid"


# Schéma utilisé pour mettre à jour partiellement un lieu existant
class PlaceUpdateSchema(BaseModel):
    title: Optional[constr(strip_whitespace=True, min_length=1, max_length=100)] = None  # type: ignore
    description: Optional[constr(strip_whitespace=True, max_length=255)] = None  # type: ignore
    price: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    owner_id: Optional[str] = None
    amenities: Optional[List[str]] = None  # liste d’IDs d’amenities

    class Config:
        extra = "forbid"


# Schéma de réponse utilisé pour retourner les données d’un lieu
class PlaceResponseSchema(BaseModel):
    id: str
    title: str
    description: str
    price: int
    latitude: float
    longitude: float
    owner_id: str
    amenities: List[str]  # <-- Liste des noms, plus des IDs
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
            amenities=[a.name for a in place.amenities],  # <--- ICI
            created_at=str(place.created_at),
            updated_at=str(place.updated_at),
        )
