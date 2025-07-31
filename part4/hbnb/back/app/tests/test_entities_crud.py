# test_entities_crud.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from app import create_app, db

class TestConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test"

class TestEntityCRUD(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class=TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

        from app.models.place import Place
        from app.models.review import Review
        from app.models.amenity import Amenity
        from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

        db.create_all()

        self.Place = Place
        self.Review = Review
        self.Amenity = Amenity
        self.place_repo = SQLAlchemyRepository(self.Place)
        self.review_repo = SQLAlchemyRepository(self.Review)
        self.amenity_repo = SQLAlchemyRepository(self.Amenity)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crud_place(self):
        # Crée d'abord un user qui sera propriétaire du lieu
        from app.models.user import User
        owner = User(
            first_name="Proprio",
            last_name="Test",
            email="owner@foo.com",
            password="x",
            is_admin=False
        )
        db.session.add(owner)
        db.session.commit()

        # Crée le lieu en lui passant owner_id
        place = self.Place(
            title="Chambre Paris",
            description="Superbe chambre au coeur de Paris",
            price=120.0,
            latitude=48.8566,
            longitude=2.3522,
            owner_id=owner.id  # FK requise
        )
        self.place_repo.add(place)
        self.assertIsNotNone(place.id)

        # Read
        fetched = self.place_repo.get(place.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.title, "Chambre Paris")

        # Update
        self.place_repo.update(place.id, {"title": "Chambre Lyon"})
        updated = self.place_repo.get(place.id)
        self.assertEqual(updated.title, "Chambre Lyon")

        # Delete
        self.place_repo.delete(place.id)
        self.assertIsNone(self.place_repo.get(place.id))

    def test_crud_review(self):
        # Création du user et du lieu requis par la Review
        from app.models.user import User
        user = User(
            first_name="Test",
            last_name="User",
            email="review@foo.com",
            password="x",
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()

        place = self.Place(
            title="LieuReview",
            description="desc",
            price=1,
            latitude=0,
            longitude=0,
            owner_id=user.id
        )
        db.session.add(place)
        db.session.commit()

        # Review avec les FK nécessaires
        review = self.Review(
            text="Génial !",
            rating=5,
            user_id=user.id,
            place_id=place.id
        )
        self.review_repo.add(review)
        self.assertIsNotNone(review.id)

        # Read
        fetched = self.review_repo.get(review.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.text, "Génial !")

        # Update
        self.review_repo.update(review.id, {"text": "Pas mal"})
        updated = self.review_repo.get(review.id)
        self.assertEqual(updated.text, "Pas mal")

        # Delete
        self.review_repo.delete(review.id)
        self.assertIsNone(self.review_repo.get(review.id))

    def test_crud_amenity(self):
        amenity = self.Amenity(name="WiFi")
        self.amenity_repo.add(amenity)
        self.assertIsNotNone(amenity.id)

        # Read
        fetched = self.amenity_repo.get(amenity.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "WiFi")

        # Update
        self.amenity_repo.update(amenity.id, {"name": "Piscine"})
        updated = self.amenity_repo.get(amenity.id)
        self.assertEqual(updated.name, "Piscine")

        # Delete
        self.amenity_repo.delete(amenity.id)
        self.assertIsNone(self.amenity_repo.get(amenity.id))

if __name__ == "__main__":
    unittest.main()
