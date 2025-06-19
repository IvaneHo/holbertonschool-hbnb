from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime


# Schéma utilisé pour valider les données d'entrée d'une review (POST/PUT)
class ReviewSchema(BaseModel):
    text: str  # Contenu de l'avis
    rating: Annotated[int, Field(ge=1, le=5)]  # Note entre 1 et 5 (inclus)
    user_id: str  # ID de l'utilisateur ayant rédigé l'avis
    place_id: str  # ID du lieu concerné par l'avis


# Schéma utilisé pour les réponses API, enrichi avec ID et timestamps
class ReviewResponseSchema(ReviewSchema):
    id: str  # Identifiant unique de la review
    created_at: datetime  # Date de création
    updated_at: datetime  # Date de dernière mise à jour
