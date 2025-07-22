
from app import db
from datetime import datetime, date, timezone
from app.models.base_model import BaseModel
  
from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

import uuid


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(60), db.ForeignKey("places.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # Relations
    user = relationship("User", back_populates="reservations")
    place = relationship("Place", back_populates="reservations")




