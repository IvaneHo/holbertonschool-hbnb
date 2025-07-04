from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig  
from flask_jwt_extended import JWTManager
db = SQLAlchemy()
jwt = JWTManager()
def create_app(config_class=DevelopmentConfig):  
    app = Flask(__name__)
    app.config.from_object(config_class)

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/hbnb_dev.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    jwt.init_app(app)
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app.models.amenity import Amenity
    # Ces imports doivent être ici
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.protected import api as protected_ns
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/",
    )
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(protected_ns, path="/api/v1/protected")
    return app
