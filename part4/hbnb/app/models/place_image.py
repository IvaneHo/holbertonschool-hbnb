from app import db
import uuid

class PlaceImage(db.Model):
    __tablename__ = "place_images"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    url = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.String(255))
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)

    def __repr__(self):
        return f"<PlaceImage {self.id} {self.url}>"
