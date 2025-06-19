from app.models.base_model import BaseModel

# Classe représentant un utilisateur de la plateforme


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        # Initialise les champs communs (id, created_at, updated_at)
        super().__init__()

        # Validation du prénom
        if not first_name or len(first_name) > 50:
            raise ValueError(
                "Le prénom est requis et doit faire max 50 caractères")

        # Validation du nom de famille
        if not last_name or len(last_name) > 50:
            raise ValueError(
                "Le nom est requis et doit faire max 50 caractères")

        # Validation de l'email (doit contenir un '@')
        if not email or "@" not in email:
            raise ValueError("Email invalide")

        # Initialisation des attributs de l'utilisateur
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin  # Indique si l'utilisateur est administrateur


# Méthode de représentation textuelle d'un objet User
def __repr__(self):
    return f"<User {self.id} {self.first_name} {self.last_name} {self.email}>"
