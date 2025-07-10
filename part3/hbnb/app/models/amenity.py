from app import db
import uuid
from datetime import datetime, timezone

class Amenity(db.Model):
    __tablename__ = "amenities"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Pas besoin de relationship() ici si déjà présent dans Place avec backref="places"

    def __repr__(self):
        return f"<Amenity {self.id} {self.name}>"
