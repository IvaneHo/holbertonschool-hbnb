import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app import db, create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def run_test():
    print("\n--- Reset base ---")
    db.drop_all()
    db.create_all()

    print("\n--- Création des objets ---")
    admin = User(first_name="Admin", last_name="Test", email="admin@hbnb.fr", password="azerty", is_admin=True)
    user = User(first_name="Jean", last_name="Client", email="jean@hbnb.fr", password="123456")
    db.session.add_all([admin, user])
    db.session.commit()

    amenity = Amenity(name="WiFi", description="Internet très rapide")
    db.session.add(amenity)
    db.session.commit()

    place = Place(
        title="Super Appart",
        description="Vue sur mer",
        price=100.0,
        latitude=48.86,
        longitude=2.34,
        owner_id=admin.id
    )
    db.session.add(place)
    db.session.commit()

    place.amenities.append(amenity)
    db.session.commit()

    review = Review(text="Incroyable séjour !", rating=5, place_id=place.id, user_id=user.id)
    db.session.add(review)
    db.session.commit()

    print("\n--- Vérification des relations ---")
    print("admin.places           :", admin.places)      # [place]
    print("user.reviews           :", user.reviews)      # [review]
    print("place.owner            :", place.owner)       # admin
    print("place.amenities        :", place.amenities)   # [amenity]
    print("amenity.places         :", amenity.places)    # [place]
    print("place.reviews          :", place.reviews)     # [review]
    print("review.place           :", review.place)      # place
    print("review.user            :", review.user)       # user

    print("\n--- Affichage détaillé ---")
    print(f"Place: {place.title}, Owner: {place.owner.email}, Amenities: {[a.name for a in place.amenities]}")
    for r in place.reviews:
        print(f"Review: {r.text} by {r.user.email}, rating={r.rating}")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        run_test()
