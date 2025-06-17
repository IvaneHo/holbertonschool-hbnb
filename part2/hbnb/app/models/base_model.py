import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Met à jour la date de modification"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Met à jour les attributs depuis un dictionnaire"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
