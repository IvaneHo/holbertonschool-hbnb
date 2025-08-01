from flask import Flask, jsonify, send_from_directory
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig  
from flask_jwt_extended import JWTManager, exceptions as jwt_exceptions
from flask_cors import CORS
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):  
    import os
    static_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'front', 'static'))
    app = Flask(__name__, static_folder=static_folder_path)
    app.config.from_object(config_class)

    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/hbnb_dev.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)  
    @app.route("/")
    def index_html():
        return send_from_directory(app.static_folder, "index.html")
    
    @app.route("/<path:filename>")
    def static_files(filename):
        # Sert tous les fichiers du dossier static (css, js, images…)
        return send_from_directory(app.static_folder, filename)
    
    # === HANDLERS D'ERREUR JWT personnalisés ===
    @app.errorhandler(jwt_exceptions.NoAuthorizationError)
    def handle_missing_auth_header(e):
        return jsonify({"error": "Le header Authorization (Bearer ...) est requis"}), 401

    @app.errorhandler(jwt_exceptions.InvalidHeaderError)
    def handle_invalid_header(e):
        return jsonify({"error": "Le header Authorization doit commencer par 'Bearer ...'"}), 401

    @app.errorhandler(jwt_exceptions.JWTDecodeError)
    def handle_jwt_decode(e):
        return jsonify({"error": "Le token JWT est invalide ou mal formé"}), 401

    # === IMPORTS LOCAUX ===
    from app.models.user import User
    from app.models.place import Place
    from app.models.review import Review
    from app.models.amenity import Amenity
    
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.reservations import api as reservations_api
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.protected import api as protected_ns

    # === CONFIG SWAGGER SECURITY ===
    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Ajouter 'Bearer <JWT>' obtenu via /auth/login"
        }
    }

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/",
        authorizations=authorizations,
        security="Bearer Auth"
    )

    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(protected_ns, path="/api/v1/protected")
    api.add_namespace(reservations_api, path="/api/v1/reservations")
    return app
