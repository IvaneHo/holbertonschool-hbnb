from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.models.review import Review

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)
