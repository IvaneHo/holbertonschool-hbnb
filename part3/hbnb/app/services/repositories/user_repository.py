from app.models.user import User
from app.persistence.repository import SQLALchemyRepository

class UserRepository(SQLALchemyRepository):
	def __init__(self):
		super().__init__(User)

	def get_user_by_email(self, email):
		return self.model.query.filter_by(email=email).first()
