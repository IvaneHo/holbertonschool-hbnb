from app import db
import uuid
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relation clean et symétrique (PAS de backref ici, on utilise back_populates)
    user = db.relationship('User', backref='reviews')
    place = db.relationship('PlaceORM', back_populates='reviews')  # 'PlaceORM', pas 'Place' !

    def __init__(self, text, rating, user, place):
        self.text = text
        self.rating = rating
        self.user = user
        self.place = place

    def __repr__(self):
        return f"<Review {self.id}: {self.text[:20]}>"
