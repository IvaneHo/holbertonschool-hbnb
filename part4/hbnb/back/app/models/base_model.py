import uuid
from datetime import datetime, timezone
from app import db

class BaseModel(db.Model):
    __abstract__ = True  # Empêche SQLAlchemy de créer une table pour BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def save(self):
        """Met à jour l'instance et enregistre dans la base"""
        self.updated_at = datetime.now(timezone.utc)
        db.session.add(self)
        db.session.commit()

    def update(self, data: dict):
        """Met à jour les attributs existants depuis un dictionnaire et sauvegarde"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()
