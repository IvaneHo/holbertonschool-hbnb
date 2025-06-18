from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Modèle d'entrée pour POST et PUT
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Modèle de réponse Swagger complet (pour GET, POST, PUT)
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='ID of the amenity'),
    'name': fields.String(required=True, description='Name of the amenity'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created', model=amenity_response_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = request.get_json()
        try:
            amenity = facade.create_amenity(data)
            return amenity, 201  # amenity est déjà un dict pydantic
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.marshal_list_with(amenity_response_model)
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        return facade.get_all_amenities(), 200


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The Amenity identifier')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully', model=amenity_response_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return {
            "id": amenity.id,
            "name": amenity.name,
            "created_at": amenity.created_at,
            "updated_at": amenity.updated_at
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully', model=amenity_response_model)
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = request.get_json()
        try:
            amenity = facade.update_amenity(amenity_id, data)
        except ValueError as e:
            return {"error": str(e)}, 400
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity, 200
