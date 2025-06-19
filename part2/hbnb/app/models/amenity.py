from app.models.base_model import BaseModel

# Classe représentant une amenity (ex. : Wi-Fi, piscine, etc.)


class Amenity(BaseModel):
    def __init__(self, name):
        # Appelle le constructeur de la classe parente (BaseModel)
        super().__init__()

        # Vérifie que le nom est fourni et ne dépasse pas 50 caractères
        if not name or len(name) > 50:
            raise ValueError(
                "Le nom de l'amenity est requis (max 50 caractères)")

        # Attribut principal : nom de l'amenity
        self.name = name
