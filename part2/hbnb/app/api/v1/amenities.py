from flask_restx import Namespace, Resource
from flask import request
from app.services.facade import facade

# Définition du namespace pour les opérations liées aux "amenities"
api = Namespace(
    "amenities",
    path="/api/v1/amenities",
    description="Amenity operations"
)


@api.route("/")
class AmenityListResource(Resource):
    def get(self):
        # Récupère et retourne la liste de toutes les amenities
        return facade.get_all_amenities(), 200

    def post(self):
        # Crée une nouvelle amenity à partir des données JSON reçues
        try:
            result = facade.create_amenity(request.json)
            return result, 201
        except ValueError as e:
            # En cas de données invalides, retourne une erreur 400
            return {"error": str(e)}, 400


@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    def get(self, amenity_id):
        # Récupère une amenity par son ID
        result = facade.get_amenity(amenity_id)
        if not result:
            # Retourne une erreur si l'amenity n'existe pas
            return {"error": "Amenity not found"}, 404
        return result, 200

    def put(self, amenity_id):
        # Met à jour une amenity existante avec les nouvelles données
        try:
            result = facade.update_amenity(amenity_id, request.json)
            if not result:
                # Si aucune amenity n'est trouvée, renvoyer une 404
                return {"error": "Amenity not found"}, 404
            return result, 200
        except ValueError as e:
            # Retourne une erreur 400 si les données sont invalides
            return {"error": str(e)}, 400
