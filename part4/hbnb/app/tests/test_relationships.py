import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import unittest
from app import db, create_app
from config import TestingConfig  # <- Ajoute ça !

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class TestRelationships(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # On passe la config DE TEST à la factory !
        cls.app = create_app(config_class=TestingConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        db.session.rollback()
        for tbl in reversed(db.metadata.sorted_tables):
            db.session.execute(tbl.delete())
        db.session.commit()

    def test_user_place_relationship(self):
        user = User(first_name="Alice", last_name="Wonder", email="alice@hbnb.fr", password="secret")
        db.session.add(user)
        db.session.commit()
        place1 = Place(title="Château", description="Beau", price=100, latitude=10, longitude=10, owner_id=user.id)
        place2 = Place(title="Cabane", description="Rustique", price=50, latitude=20, longitude=20, owner_id=user.id)
        db.session.add_all([place1, place2])
        db.session.commit()
        self.assertEqual(len(user.places), 2)
        self.assertIn(place1, user.places)
        self.assertEqual(place1.owner, user)

    def test_place_review_relationship(self):
        user = User(first_name="Bob", last_name="Test", email="bob@hbnb.fr", password="secret")
        db.session.add(user)
        db.session.commit()
        place = Place(title="Villa", description="Vue mer", price=200, latitude=12, longitude=18, owner_id=user.id)
        db.session.add(place)
        db.session.commit()
        review = Review(text="Parfait", rating=5, place_id=place.id, user_id=user.id)
        db.session.add(review)
        db.session.commit()
        self.assertIn(review, place.reviews)
        self.assertEqual(review.place, place)

    def test_user_review_relationship(self):
        user = User(first_name="Eve", last_name="Feedback", email="eve@hbnb.fr", password="secret")
        db.session.add(user)
        db.session.commit()
        place = Place(title="Loft", description="Moderne", price=130, latitude=15, longitude=22, owner_id=user.id)
        db.session.add(place)
        db.session.commit()
        review = Review(text="Bien situé", rating=4, place_id=place.id, user_id=user.id)
        db.session.add(review)
        db.session.commit()
        self.assertIn(review, user.reviews)
        self.assertEqual(review.user, user)

    def test_place_amenity_many_to_many(self):
        user = User(first_name="Sam", last_name="Demo", email="sam@hbnb.fr", password="secret")
        db.session.add(user)
        db.session.commit()
        place = Place(title="Igloo", description="Froid", price=80, latitude=50, longitude=1, owner_id=user.id)
        db.session.add(place)
        db.session.commit()
        amenity1 = Amenity(name="Jacuzzi", description="Chaud !")
        amenity2 = Amenity(name="Bar", description="Boissons incluses")
        db.session.add_all([amenity1, amenity2])
        db.session.commit()
        place.amenities.append(amenity1)
        place.amenities.append(amenity2)
        db.session.commit()
        self.assertIn(amenity1, place.amenities)
        self.assertIn(amenity2, place.amenities)
        self.assertIn(place, amenity1.places)
        self.assertIn(place, amenity2.places)

    def test_foreign_keys_and_constraints(self):
        user = User(first_name="Joe", last_name="Root", email="joe@hbnb.fr", password="root")
        db.session.add(user)
        db.session.commit()
        place = Place(title="Cottage", description="Cosy", price=70, latitude=7, longitude=7, owner_id=user.id)
        db.session.add(place)
        db.session.commit()
        with self.assertRaises(Exception):
            review = Review(text="No place!", rating=3, place_id=None, user_id=user.id)
            db.session.add(review)
            db.session.commit()
            db.session.rollback()

    def test_schema_is_created(self):
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        for t in ["users", "places", "reviews", "amenities", "place_amenity"]:
            self.assertIn(t, tables)

if __name__ == "__main__":
    unittest.main()
