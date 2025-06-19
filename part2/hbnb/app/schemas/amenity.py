from pydantic import BaseModel, constr  # type: ignore
from datetime import datetime

# Schéma Pydantic utilisé pour la validation des données d’entrée
# (création/mise à jour)


class AmenitySchema(BaseModel):
    # Le nom doit être une chaîne non vide, max 50 caractères, avec espaces en
    # trop supprimés
    name: constr(strip_whitespace=True, max_length=50)  # type: ignore

# Schéma de réponse étendu avec des champs système (ID, timestamps)


class AmenityResponseSchema(AmenitySchema):
    id: str  # Identifiant unique de l'amenity
    created_at: datetime  # Date de création
    updated_at: datetime  # Date de dernière modification
