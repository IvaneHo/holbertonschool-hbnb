from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

# Liste des domaines bannis
BANNED_DOMAINS = {
    "mailinator.com", "10minutemail.com", "tempmail.com",
    "guerrillamail.com", "yopmail.com", "dispostable.com"
}

class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    @field_validator('email')
    @classmethod
    def validate_email_domain(cls, value: EmailStr) -> EmailStr:
        domain = value.split('@')[-1].lower()
        if '.' not in domain:
            raise ValueError("L'email doit contenir un point dans le domaine (ex: exemple.com)")
        if domain in BANNED_DOMAINS:
            raise ValueError(f"Domaine email interdit : {domain}")
        return value


class UserResponseSchema(UserSchema):
    id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    is_admin: Optional[bool] = False

    class Config:
        # Pydantic v2 : mode strict pour éviter de mal sérialiser
        from_attributes = True
