import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app import create_app, db
from app.models.user import User

def create_admin():
    admin_email = "admin@hbnb.fr"
    admin_password = "12345678"
    # Supprime tout admin existant pour garantir le hashage clean
    admin = User.query.filter_by(email=admin_email).first()
    if admin:
        db.session.delete(admin)
        db.session.commit()

    admin = User(
        first_name="Admin",
        last_name="HBNB",
        email=admin_email,
        password=admin_password,  # Mot de passe EN CLAIR
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print(f"Admin créé/réinitialisé : {admin_email}")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        create_admin()
