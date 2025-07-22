import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest

from app import create_app, db
from app.models.user import User
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository


def test_sqlalchemy_repository_init_and_methods():
    """Test structure and basic instantiation of SQLAlchemyRepository."""

    app = create_app()

    # Vérifie que le repo s'instancie sans erreur
    repo = SQLAlchemyRepository(User)
    assert repo.model is User

    # Teste que toutes les méthodes existent bien
    assert hasattr(repo, 'add')
    assert hasattr(repo, 'get')
    assert hasattr(repo, 'get_all')
    assert hasattr(repo, 'update')
    assert hasattr(repo, 'delete')
    assert hasattr(repo, 'get_by_attribute')

    # Ces appels ne fonctionneront pas tant que la base n'est pas créée,
    # mais doivent lever des erreurs SQLAlchemy si on tente d'appeler sans mapping.
    with app.app_context():
        try:
            repo.get("fake_id")
        except Exception as e:
            print("Pas encore mappé (normal):", e)

    print("SQLAlchemyRepository structure OK ✅")

if __name__ == "__main__":
    test_sqlalchemy_repository_init_and_methods()
    print("Test SQLAlchemyRepository terminé.")
