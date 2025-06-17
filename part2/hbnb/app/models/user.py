from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

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
def __repr__(self):
    return f"<User {self.id} {self.first_name} {self.last_name} {self.email}>"
