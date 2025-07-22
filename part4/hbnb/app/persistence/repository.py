from abc import ABC, abstractmethod
from datetime import datetime, timezone




class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        # Ajoute un objet au repository
        pass

    @abstractmethod
    def get(self, obj_id):
        # Récupère un objet par son identifiant
        pass

    @abstractmethod
    def get_all(self):
        # Récupère tous les objets stockés
        pass

    @abstractmethod
    def update(self, obj_id, data):
        # Met à jour un objet existant avec des données
        pass

    @abstractmethod
    def delete(self, obj_id):
        # Supprime un objet du repository par son ID
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        # Récupère un objet en fonction d’un attribut spécifique
        pass



class InMemoryRepository(Repository):
    def __init__(self):
        # Stockage interne des objets par ID
        self._storage = {}

    def add(self, obj):
        # Ajoute l'objet en l'indexant par son ID
        self._storage[obj.id] = obj

    def get(self, obj_id):
        # Retourne l'objet correspondant à l'ID (ou None)
        return self._storage.get(obj_id)

    def get_all(self):
        # Retourne une liste de tous les objets stockés
        return list(self._storage.values())

    def update(self, obj_id, data):
        # Met à jour un objet existant avec les nouvelles données
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            # Met à jour la date de dernière modification
            obj.updated_at = self._now()

    def delete(self, obj_id):
        # Supprime l'objet du stockage s'il existe
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        # Recherche le premier objet ayant l’attribut correspondant
        return next(
            (
                obj
                for obj in self._storage.values()
                if getattr(obj, attr_name) == attr_value
            ),
            None,
        )

    def _now(self):
        # Retourne l'heure actuelle UTC
        return datetime.now(timezone.utc)()
