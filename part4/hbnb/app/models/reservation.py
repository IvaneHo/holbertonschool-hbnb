from app import db
from datetime import date
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship

class Reservation(BaseModel, db.Model):
    __tablename__ = 'reservations'

    user_id = db.Column(db.String(60), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(60), db.ForeignKey("places.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")

    # Relations
    user = relationship("User", back_populates="reservations")
    place = relationship("Place", back_populates="reservations")
