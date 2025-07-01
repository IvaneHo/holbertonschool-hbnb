import uuid
from datetime import datetime

# Classe de base commune à tous les modèles (gère ID et timestamps)


class BaseModel:
    def __init__(self):
        # Génère un identifiant unique pour chaque instance
        self.id = str(uuid.uuid4())

        # Date de création de l'objet
        self.created_at = datetime.now()

        # Date de dernière mise à jour (initialisée à la création)
        self.updated_at = datetime.now()

    def save(self):
        """Met à jour la date de modification"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Met à jour les attributs depuis un dictionnaire"""
        for key, value in data.items():
            if hasattr(self, key):
                # Modifie uniquement les attributs existants
                setattr(self, key, value)
        # Met à jour la date de modification après les changements
        self.save()
