from datetime import date
from pydantic import BaseModel, model_validator

class ReservationCreateSchema(BaseModel):
    place_id: str
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def check_dates(cls, values):
        start = values.get('start_date')
        end = values.get('end_date')
        if start and end and end <= start:
            raise ValueError("La date de fin doit être après la date de début.")
        return values

class ReservationUpdateSchema(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = None

    @model_validator(mode="after")
    def check_dates(cls, values):
        start = values.get('start_date')
        end = values.get('end_date')
        if start and end and end <= start:
            raise ValueError("La date de fin doit être après la date de début.")
        return values

class ReservationResponseSchema(BaseModel):
    id: str
    user_id: str
    place_id: str
    start_date: date
    end_date: date
    status: str
    created_at: str | None = None
    updated_at: str | None = None
