from app.models.base_model import BaseModel

# Classe représentant un lieu (ex : maison, appartement à louer)


class Place(BaseModel):
    def __init__(self, title, description, price,
                 latitude, longitude, owner):
        # Appelle le constructeur de BaseModel (gère ID et dates)
        super().__init__()

        # Vérifications des contraintes métier
        if not title or len(title) > 100:
            raise ValueError(
                "Le titre est requis et doit faire max 100 caractères")
        if price <= 0:
            raise ValueError("Le prix doit être un nombre positif")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude invalide")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude invalide")

        # Affectation des attributs de l'instance
        self.title = title
        self.description = description or ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # objet User associé
        self.reviews = []  # liste des objets Review
        self.amenities = []  # liste des objets Amenity

    def add_review(self, review):
        # Ajoute un avis (Review) à la liste associée
        self.reviews.append(review)

    def add_amenity(self, amenity):
        # Ajoute une amenity à la liste associée
        self.amenities.append(amenity)
