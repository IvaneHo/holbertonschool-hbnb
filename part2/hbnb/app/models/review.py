from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text:
            raise ValueError("Le texte de l'avis est requis")
        if not (1 <= rating <= 5):
            raise ValueError("La note doit être entre 1 et 5")

        self.text = text
        self.rating = rating
        self.place = place  # Objet Place
        self.user = user    # Objet User

    @property
    def place_id(self):
        return self.place.id if self.place else None

    @property
    def user_id(self):
        return self.user.id if self.user else None
