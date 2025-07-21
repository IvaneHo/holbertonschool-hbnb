from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime



# Schéma utilisé pour la création d’un utilisateur (avec mot de passe)
class UserCreateSchema(BaseModel):
    first_name: str  # Prénom requis
    last_name: str   # Nom requis
    email: EmailStr  # Email valide
    password: str    # Mot de passe requis

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value: EmailStr) -> EmailStr:
        domain = value.split("@")[-1].lower()
        if "." not in domain:
            raise ValueError(
                "L'email doit contenir un point dans le domaine (ex: exemple.com)"
            )
        

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
        
        return value

# Schéma pour la modification (update), mot de passe optionnel
class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None  # Peut être changé

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value: EmailStr) -> EmailStr:
        domain = value.split("@")[-1].lower()
        if "." not in domain:
            raise ValueError("L'email doit contenir un point dans le domaine")
       

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if value is not None and len(value) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
        return value


class UserResponseSchema(BaseModel):
    id: Optional[str]
    first_name: str
    last_name: str
    email: EmailStr
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    is_admin: Optional[bool] = False

    class Config:
        from_attributes = True  

