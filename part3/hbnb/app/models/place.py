# === Modèle métier (logique Python, pas relié à SQLAlchemy) ===
from app.models.base_model import BaseModel
from typing import List, Optional

class Place(BaseModel):
    """
    Modèle métier Place utilisé côté services/facade, non directement lié à la base SQL.
    """
    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner,
        amenities: Optional[List] = None,
        id: Optional[str] = None
    ):
        super().__init__()
        self.id = id  # Pour compatibilité mapping

        if not title or len(title) > 100:
            raise ValueError("Le titre est requis et doit faire max 100 caractères")
        if price <= 0:
            raise ValueError("Le prix doit être un nombre positif")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude invalide")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude invalide")

        self.title = title
        self.description = description or ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # objet User ou owner_id
        self.reviews = []   # Liste de Review (objet métier)
        self.amenities = amenities if amenities is not None else []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)


# === Modèle ORM SQLAlchemy (mapping table places) ===

import uuid
from datetime import datetime

try:
    from app import db
except ImportError:
    db = None

if db is not None:
    class PlaceORM(db.Model):
        __tablename__ = "places"
        id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        title = db.Column(db.String(100), nullable=False)
        description = db.Column(db.Text)
        price = db.Column(db.Float, nullable=False)
        latitude = db.Column(db.Float, nullable=False)
        longitude = db.Column(db.Float, nullable=False)
        owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        # Ici, on met reviews <-> place (back_populates, PAS backref)
        reviews = db.relationship('Review', back_populates='place', lazy='dynamic')

        def __repr__(self):
            return f"<PlaceORM {self.id} {self.title}>"

