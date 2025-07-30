from pydantic import BaseModel, constr
from typing import Optional, List
from app.models.place import Place

# --- Pour une image ---
class PlaceImageSchema(BaseModel):
    url: str
    caption: Optional[str] = None

# --- Pour création d'une place (request) ---
class PlaceSchema(BaseModel):
    title: constr(strip_whitespace=True, min_length=1, max_length=100) # type: ignore
    description: constr(strip_whitespace=True, max_length=255) # type: ignore
    price: float
    latitude: float
    longitude: float
    owner_id: str
    amenities: List[str]
    images: Optional[List[PlaceImageSchema]] = None  

    class Config:
        extra = "forbid"

# --- Pour update (request PATCH/PUT) ---
class PlaceUpdateSchema(BaseModel):
    title: Optional[constr(strip_whitespace=True, min_length=1, max_length=100)] = None # type: ignore
    description: Optional[constr(strip_whitespace=True, max_length=255)] = None # type: ignore
    price: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    owner_id: Optional[str] = None
    amenities: Optional[List[str]] = None
    images: Optional[List[PlaceImageSchema]] = None  # Optionnel pour PATCH aussi

    class Config:
        extra = "forbid"

# --- Pour réponse (response GET) ---
class PlaceResponseSchema(BaseModel):
    id: str
    title: str
    description: str
    price: float
    latitude: float
    longitude: float
    owner_id: str
    amenities: List[str]
    images: List[PlaceImageSchema] = []
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
            owner_id=getattr(place, "owner_id", None),
            amenities=[a.name for a in getattr(place, "amenities", [])],
            images=[PlaceImageSchema(url=img.url, caption=img.caption) for img in getattr(place, "images", [])],
            created_at=str(place.created_at),
            updated_at=str(place.updated_at),
        )
