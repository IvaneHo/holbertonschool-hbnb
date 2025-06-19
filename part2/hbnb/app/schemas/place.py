from pydantic import BaseModel, condecimal, constr, conlist  # type: ignore
from typing import Optional, List
from datetime import datetime
from app.models.place import Place


# Schéma de réponse Pydantic utilisé pour retourner les données d’un lieu
class PlaceResponseSchema(BaseModel):
    id: str  # Identifiant unique du lieu
    title: str  # Titre du lieu
    description: str  # Description textuelle
    price: int  # Prix par nuit (en entier)
    latitude: float  # Coordonnée latitude (-90 à 90)
    longitude: float  # Coordonnée longitude (-180 à 180)
    owner_id: str  # ID de l'utilisateur propriétaire
    amenities: List[str]  # Liste des IDs des amenities associées
    created_at: str  # Date de création
    updated_at: str  # Date de dernière modification

    @classmethod
    def from_place(cls, place: Place) -> "PlaceResponseSchema":
        # Fabrique une instance du schéma à partir d’un objet Place
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
