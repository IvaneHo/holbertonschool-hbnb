from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import facade

api = Namespace("amenities", path="/api/v1/amenities", description="Amenity operations")

amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(required=True, description="Name of the amenity"),
        "description": fields.String(
            required=False, description="Description of the amenity"
        ),
    },
)

amenity_partial_model = api.model(
    "AmenityPartial",
    {
        "name": fields.String(description="Name (optional)"),
        "description": fields.String(description="Description (optional)"),
    },
)

amenity_response_model = api.inherit(
    "AmenityResponse",
    amenity_model,
    {
        "id": fields.String(description="Unique amenity ID"),
        "created_at": fields.DateTime(description="Creation timestamp"),
        "updated_at": fields.DateTime(description="Last update timestamp"),
    },
)

@api.route("/")
class AmenityListResource(Resource):
    @api.marshal_with(amenity_response_model, as_list=True)
    def get(self):
        """Retrieve all amenities"""
        amenities = facade.get_all_amenities()  
        return amenities, 200

    @api.expect(amenity_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a new amenity (admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        data = request.get_json(force=True)
        if not data or not data.get("name") or not data.get("name").strip():
            return {"error": "name is required (max 50 characters)"}, 400
        try:
            result = facade.create_amenity(data)  
            return result, 201
        except Exception as e:
            return {"error": str(e)}, 400

@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    def get(self, amenity_id):
        """Retrieve a specific amenity by its ID"""
        result = facade.get_amenity(amenity_id)
        if not result or result.get("id") is None:
            return {"error": "Amenity not found"}, 404
        return result, 200  

    @api.expect(amenity_partial_model, validate=True)
    @jwt_required()
    def put(self, amenity_id):
        """Update an existing amenity (admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        result = facade.get_amenity(amenity_id)
        if not result or result.get("id") is None:
            return {"error": "Amenity not found"}, 404
        try:
            updated = facade.update_amenity(amenity_id, request.json)
            return updated, 200 
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, "Amenity deleted")
    @api.response(404, "Amenity not found")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def delete(self, amenity_id):
       """Delete an amenity (admin only)"""
       claims = get_jwt()
       if not claims.get("is_admin"):
          return {"error": "Admin privileges required"}, 403

       result = facade.get_amenity(amenity_id)
       if not result or result.get("id") is None:
         return {"error": "Amenity not found"}, 404

       try:
           facade.delete_amenity(amenity_id)
           
           return {"message": "Amenity deleted successfully"}, 200
       except Exception as e:
           return {"error": str(e)}, 400

