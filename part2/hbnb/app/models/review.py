from app.models.base_model import BaseModel

# Classe représentant un avis (review) laissé par un utilisateur sur un lieu


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        # Initialise les attributs hérités (id, created_at, updated_at)
        super().__init__()

        # Vérifie que le texte est fourni
        if not text:
            raise ValueError("Le texte de l'avis est requis")
        # Vérifie que la note est comprise entre 1 et 5
        if not (1 <= rating <= 5):
            raise ValueError("La note doit être entre 1 et 5")

        # Affecte les attributs spécifiques à la review
        self.text = text
        self.rating = rating
        self.place = place  # Objet Place lié à cet avis
        self.user = user    # Objet User auteur de l'avis

    @property
    def place_id(self):
        # Retourne l'ID du lieu associé (ou None si non défini)
        return self.place.id if self.place else None

    @property
    def user_id(self):
        # Retourne l'ID de l'utilisateur auteur (ou None si non défini)
        return self.user.id if self.user else None
