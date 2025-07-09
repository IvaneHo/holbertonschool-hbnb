import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from app import create_app, db
from app.models.user import User
from app.persistence.user_repository import UserRepository
import uuid

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        # Set up a fresh app and DB before each test
        self.app = create_app()
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["TESTING"] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all() 
        print("DB URI utilisée pour le test:", self.app.config["SQLALCHEMY_DATABASE_URI"])
        db.create_all()
        self.repo = UserRepository()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crud_user(self):
        # Create user
        user = User(
            first_name="Alice",
            last_name="Liddell",
            email="alice@example.com",
            password="hashed_pwd",
            is_admin=True
        )
        self.repo.add(user)
        self.assertIsNotNone(user.id)

        # Get user by id
        fetched = self.repo.get(user.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.email, "alice@example.com")

        # Get user by email
        fetched2 = self.repo.get_user_by_email("alice@example.com")
        self.assertIsNotNone(fetched2)
        self.assertEqual(fetched2.first_name, "Alice")

        # Update user
        self.repo.update(user.id, {"first_name": "Alicia"})
        updated = self.repo.get(user.id)
        self.assertEqual(updated.first_name, "Alicia")

        # Get all users
        users = self.repo.get_all()
        self.assertEqual(len(users), 1)

        # Delete user
        self.repo.delete(user.id)
        self.assertIsNone(self.repo.get(user.id))

if __name__ == "__main__":
    unittest.main()
