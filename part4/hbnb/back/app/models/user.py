from app.models.base_model import BaseModel
from app import db
from argon2 import PasswordHasher

ph = PasswordHasher()

class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # --- RELATIONS ---
    places = db.relationship(
        "Place",
        backref="owner",
        cascade="all, delete-orphan",
        lazy='selectin'
    )
    reviews = db.relationship(
        "Review",
        backref="user",
        cascade="all, delete-orphan",
        lazy='selectin'
    )
    reservations = db.relationship("Reservation", back_populates="user")

    def __init__(self, first_name, last_name, email, password, is_admin=False):
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

    def hash_password(self, plain_password):
        """Hash le mot de passe avec Argon2 et le stocke."""
        self.password = ph.hash(plain_password)

    def verify_password(self, plain_password):
        """Vérifie si le mot de passe en clair correspond au hash."""
        try:
            return ph.verify(self.password, plain_password)
        except Exception:
            return False

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name} {self.email}>"
