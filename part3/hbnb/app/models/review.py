from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        # Validation
        if not text:
            raise ValueError("Le texte de l'avis est requis")
        if not (1 <= rating <= 5):
            raise ValueError("La note doit être entre 1 et 5")
        if not place or not user:
            raise ValueError("Un utilisateur et un lieu sont requis")

        # Attributs simples (indispensables pour Pydantic, JSON, etc.)
        self.text = text
        self.rating = rating
        self.place_id = place.id
        self.user_id = user.id
        self.created_at = self.created_at  # hérité de BaseModel
        self.updated_at = self.updated_at  # hérité de BaseModel
