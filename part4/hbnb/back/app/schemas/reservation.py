from datetime import date
from pydantic import BaseModel, model_validator

class ReservationCreateSchema(BaseModel):
    place_id: str
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValueError("La date de fin doit être après la date de début.")
        return self

class ReservationUpdateSchema(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = None

    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValueError("La date de fin doit être après la date de début.")
        return self

class ReservationResponseSchema(BaseModel):
    id: str
    user_id: str
    place_id: str
    start_date: date
    end_date: date
    status: str
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_orm_reservation(cls, reservation):
        print("DEBUG ORM:", vars(reservation))
        return cls(
            id=reservation.id,
            user_id=reservation.user_id,
            place_id=reservation.place_id,
            start_date=reservation.start_date,
            end_date=reservation.end_date,
            status=reservation.status,
            created_at=str(reservation.created_at) if reservation.created_at else None,
            updated_at=str(reservation.updated_at) if reservation.updated_at else None
        )
