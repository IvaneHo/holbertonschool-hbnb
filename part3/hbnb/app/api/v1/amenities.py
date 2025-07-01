from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade

# Define the namespace for amenity-related operations
api = Namespace("amenities", path="/api/v1/amenities", description="Amenity operations")

# Model used in Swagger for creation (POST)
amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(required=True, description="Name of the amenity"),
        "description": fields.String(
            required=False, description="Description of the amenity"
        ),
    },
)

# Model used in Swagger for partial update (PUT)
amenity_partial_model = api.model(
    "AmenityPartial",
    {
        "name": fields.String(description="Name (optional)"),
        "description": fields.String(description="Description (optional)"),
    },
)

# Response model used in Swagger (GET, POST, PUT)
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
        return facade.get_all_amenities(), 200

    @api.expect(amenity_model, validate=True)
    def post(self):
        """Create a new amenity"""
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
        # Correction ici : on vérifie aussi si result.get("id") est None
        if not result or result.get("id") is None:
            return {"error": "Amenity not found"}, 404
        return result, 200

    @api.expect(amenity_partial_model, validate=True)
    def put(self, amenity_id):
        """Update an existing amenity (partial updates allowed)"""
        result = facade.get_amenity(amenity_id)
        if not result or result.get("id") is None:
            return {"error": "Amenity not found"}, 404
        try:
            result = facade.update_amenity(amenity_id, request.json)
            return result, 200
        except Exception as e:
            return {"error": str(e)}, 400
