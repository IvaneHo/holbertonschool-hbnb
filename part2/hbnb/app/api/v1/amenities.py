#!/usr/bin/python3


from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
api = Namespace('amenities', description='Amenity operations')
# Modèle de requête
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})
@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = request.get_json()
        try:
            amenity = facade.create_amenity(data)
            return {"id": amenity.id, "name": amenity.name}, 201
        except ValueError as e:
            return {"error": str(e)}, 400
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{"id": a.id, "name": a.name} for a in amenities], 200
@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The Amenity identifier')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return {"id": amenity.id, "name": amenity.name}, 200
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
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
        return {"id": amenity.id, "name": amenity.name}, 200