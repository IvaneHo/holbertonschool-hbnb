from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.models.place_image import PlaceImage

class PlaceImageRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(PlaceImage)
