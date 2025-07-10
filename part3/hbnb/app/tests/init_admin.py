import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app import create_app, db
from app.models.user import User

def create_admin():
    admin_email = "admin@hbnb.fr"
    admin_password = "12345678"  # mets un mot de passe fort ou en variable d'env
    # Vérifie si un admin existe déjà
    existing = User.query.filter_by(email=admin_email).first()
    if existing:
        print(f"L'admin {admin_email} existe déjà.")
        return

    admin = User(
        first_name="Admin",
        last_name="HBNB",
        email=admin_email,
        password=admin_password,
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print(f"Admin créé : {admin_email}")

if __name__ == "__main__":
    # --- C'est cette ligne qui change tout ---
    app = create_app()  # ← ou l'import de ton objet app si il existe
    with app.app_context():
        create_admin()