# create_tables.py

from app import create_app
from app import db  # <- adapte si 'db' est ailleurs !

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tables créées !")
