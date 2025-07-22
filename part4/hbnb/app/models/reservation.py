
from app import db
from datetime import datetime, date, timezone
from app.models.base_model import BaseModel
  
from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Reservation(BaseModel):
    __tablename__ = "reservations"
    id = db.Column(String(60), primary_key=True)
    user_id = db.Column(String(60), ForeignKey('users.id'), nullable=False)
    place_id = db.Column(String(60), ForeignKey('places.id'), nullable=False)
    start_date = db.Column(Date, nullable=False)
    end_date = db.Column(Date, nullable=False)
    status = db.Column(String(20), nullable=False, default='pending')
    created_at = db.Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relations
    user = relationship("User", back_populates="reservations")
    place = relationship("Place", back_populates="reservations")
