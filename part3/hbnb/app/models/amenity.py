from app.models.base_model import BaseModel

# Classe métier (logique Python pure)
class Amenity(BaseModel):
    def __init__(self, name: str, description: str = ""):
        super().__init__()

        if not name or len(name.strip()) > 50:
            raise ValueError("Le nom de l'amenity est requis (max 50 caractères)")

        self.name = name.strip()
        self.description = description.strip() if description else ""


# ==== Modèle SQLAlchemy ORM pour la persistance ====

import uuid
from datetime import datetime

try:
    from app import db
except ImportError:
    db = None

if db is not None:
    class AmenityORM(db.Model):
        __tablename__ = "amenities"
        id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        name = db.Column(db.String(50), nullable=False)
        description = db.Column(db.Text)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

        def __repr__(self):
            return f"<AmenityORM {self.id} {self.name}>"
