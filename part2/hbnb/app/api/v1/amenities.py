from flask_restx import Namespace, Resource
from flask import request
from app.services.facade import facade

api = Namespace("amenities", path="/api/v1/amenities", description="Amenity operations")



@api.route("/")
class AmenityListResource(Resource):
    def get(self):
        return facade.get_all_amenities(), 200

    def post(self):
        try:
            result = facade.create_amenity(request.json)
            return result, 201
        except ValueError as e:
            return {"error": str(e)}, 400


@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    def get(self, amenity_id):
        result = facade.get_amenity(amenity_id)
        if not result:
            return {"error": "Amenity not found"}, 404
        return result, 200

    def put(self, amenity_id):
        try:
            result = facade.update_amenity(amenity_id, request.json)
            if not result:
                return {"error": "Amenity not found"}, 404
            return result, 200
        except ValueError as e:
            return {"error": str(e)}, 400
