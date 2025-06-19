from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

# Liste des domaines email jetables interdits
BANNED_DOMAINS = {
    "mailinator.com", "10minutemail.com", "tempmail.com",
    "guerrillamail.com", "yopmail.com", "dispostable.com"
}


# Schéma utilisé pour valider les données d’entrée d’un utilisateur
class UserSchema(BaseModel):
    first_name: str  # Prénom requis
    last_name: str   # Nom requis
    email: EmailStr  # Email au format valide (grâce à Pydantic)

    @field_validator('email')
    @classmethod
    def validate_email_domain(cls, value: EmailStr) -> EmailStr:
        # Valide que l’email contient un domaine correct
        domain = value.split('@')[-1].lower()
        if '.' not in domain:
            raise ValueError(
                "L'email doit contenirunpointdansle domaine (ex: exemple.com)")
        if domain in BANNED_DOMAINS:
            raise ValueError(f"Domaine email interdit : {domain}")
        return value


# Schéma enrichi utilisé pour les réponses API (inclut ID, timestamps, etc.)
class UserResponseSchema(UserSchema):
    id: Optional[str]  # ID de l'utilisateur
    created_at: Optional[datetime]  # Date de création
    updated_at: Optional[datetime]  # Dernière mise à jour
    is_admin: Optional[bool] = False  # Statut administrateur (facultatif)

    class Config:
        # Permet à Pydantic d’accepter les objets avec attributs comme
        # `user.first_name`
        from_attributes = True
