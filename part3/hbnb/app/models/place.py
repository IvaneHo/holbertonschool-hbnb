from app import db
import uuid
from datetime import datetime


# Table d'association Many-to-Many Place <-> Amenity
place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True)
)



class Place(db.Model):
    __tablename__ = "places"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        backref="places",
        lazy='selectin'  # améliore les requêtes massives
)

    
    
    def __repr__(self):
        return f"<Place {self.id} {self.title}>"
