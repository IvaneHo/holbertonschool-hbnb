from app import db
from argon2 import PasswordHasher
from .base_model import BaseModel
from datetime import datetime
import uuid

ph = PasswordHasher()

class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        # Validations identiques à avant
        if not first_name or len(first_name) > 50:
            raise ValueError("Le prénom est requis et doit faire max 50 caractères")
        if not last_name or len(last_name) > 50:
            raise ValueError("Le nom est requis et doit faire max 50 caractères")
        if not email or "@" not in email:
            raise ValueError("Email invalide")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)
        # id, created_at, updated_at gérés automatiquement

    def hash_password(self, password):
        """Hash le mot de passe avec Argon2 et le stocke."""
        self.password = ph.hash(password)

    def verify_password(self, password):
        """Vérifie si le mot de passe en clair correspond au hash."""
        try:
            return ph.verify(self.password, password)
        except Exception:
            return False

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name} {self.email}>"
