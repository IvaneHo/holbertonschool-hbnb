from app.models.base_model import BaseModel

# Classe représentant une amenity (ex. : Wi-Fi, piscine, etc.)


class Amenity(BaseModel):
    def __init__(self, name: str, description: str = ""):
        super().__init__()

        if not name or len(name.strip()) > 50:
            raise ValueError("Le nom de l'amenity est requis (max 50 caractères)")

        self.name = name.strip()
        self.description = description.strip() if description else ""
