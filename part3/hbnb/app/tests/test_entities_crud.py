import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unittest
from app import create_app, db

class TestEntityCRUD(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["TESTING"] = True
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Import des modèles et repo APRES context et config
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
        place = self.Place(
            title="Chambre Paris",
            description="Superbe chambre au coeur de Paris",
            price=120.0,
            latitude=48.8566,
            longitude=2.3522
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
        review = self.Review(
            text="Génial !",
            rating=5,
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
