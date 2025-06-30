from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade

# Définition du namespace pour les opérations liées aux "amenities"
api = Namespace(
    "amenities",
    path="/api/v1/amenities",
    description="Amenity operations"
)

amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='Amenity unique ID'),
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route("/")
class AmenityListResource(Resource):
    @api.doc('List_amenities')
    @api.marshal_list_with(amenity_model)
    def get(self):
        # Récupère et retourne la liste de toutes les amenities
        return facade.get_all_amenities(), 200
    
    @api.doc('create_amenity')
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid data')
    def post(self):
        # Crée une nouvelle amenity à partir des données JSON reçues
        try:
            result = facade.create_amenity(request.json)
            return result, 201
        except ValueError as e:
            # En cas de données invalides, retourne une erreur 400
            return {"error": str(e)}, 400


@api.route("/<string:amenity_id>")
@api.param('amenity_id', 'Amenity identifier')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        # Récupère une amenity par son ID
        result = facade.get_amenity(amenity_id)
        if not result:
            # Retourne une erreur si l'amenity n'existe pas
            return {"error": "Amenity not found"}, 404
        return result, 200
    
    @api.doc('update_amenity')
    @api.expect(amenity_model)
    @api.response(200, 'Amenity successfully updated')
    @api.response(400, 'Invalid input')
    @api.response(404, 'Amenity not found')
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
