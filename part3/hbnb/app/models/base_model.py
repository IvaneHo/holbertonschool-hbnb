import uuid
from datetime import datetime
from app import db

class BaseModel(db.Model):
    __abstract__ = True  # Empêche SQLAlchemy de créer une table pour BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def save(self):
        """Met à jour l'instance et enregistre dans la base"""
        self.updated_at = datetime.now()
        db.session.add(self)
        db.session.commit()

    def update(self, data: dict):
        """Met à jour les attributs existants depuis un dictionnaire et sauvegarde"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
        db.session.commit()
