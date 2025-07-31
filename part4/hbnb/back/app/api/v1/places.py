from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade
from app.models.place import Place
from app.schemas.place import PlaceResponseSchema

api = Namespace("places", description="Place operations")

def get_current_user_id():
    """Gère JWT str ou dict selon la config"""
    ident = get_jwt_identity()
    return ident if isinstance(ident, str) else ident.get("id")



#  MODELS 

place_image_model = api.model(
    "PlaceImage",
    {
        "url": fields.String(required=True, description="URL of the image"),
        "caption": fields.String(description="Image caption", required=False),
    }
)

place_model = api.model(
    "Place",
    {
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night (non-negative)"),
        "latitude": fields.Float(required=True, description="Latitude between -90 and 90"),
        "longitude": fields.Float(required=True, description="Longitude between -180 and 180"),
        "amenities": fields.List(fields.String, required=True, description="List of Amenity IDs"),
        "images": fields.List(fields.Nested(place_image_model), required=False, description="List of images (url/caption)"),
    },
)

place_update_model = api.model(
    "PlaceUpdate",
    {
        "title": fields.String(description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(description="Price per night (non-negative)"),
        "latitude": fields.Float(description="Latitude between -90 and 90"),
        "longitude": fields.Float(description="Longitude between -180 and 180"),
        "amenities": fields.List(fields.String, description="List of Amenity IDs"),
        "images": fields.List(fields.Nested(place_image_model), required=False, description="List of images (url/caption)"),
    },
)

# ROUTES

@api.route("/")
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.doc(description="Create a new place (auth required, owner set automatically)")
    @jwt_required()
    def post(self):
        """Create a new place (owner is always the current user)"""
        data = api.payload.copy()
        data["owner_id"] = get_current_user_id()
        try:
            result = facade.create_place(data)
            return result, 201
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, "List of all places retrieved")
    @api.doc(description="Retrieve the full list of places (public endpoint)")
    def get(self):
        """Retrieve all places (public)"""
        places = facade.get_all_places() 
        return list(places), 200


@api.route("/<string:place_id>")
class PlaceResource(Resource):
    @api.response(200, "Place retrieved successfully")
    @api.response(404, "Place not found")
    @api.doc(description="Get a place by its ID (public endpoint)")
    def get(self, place_id):
        """Get a place by ID (public)"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place, 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, "Place successfully updated")
    @api.response(404, "Place not found")
    @api.response(400, "Validation error")
    @api.response(403, "Unauthorized action")
    @api.doc(description="Update a place by its ID. Owner or admin only.")
    @jwt_required()
    def put(self, place_id):
        """Update a place by ID (owner or admin only)"""
        user_id = get_current_user_id()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        if not is_admin and place["owner_id"] != user_id:
            return {"error": "Unauthorized action"}, 403

        payload = api.payload.copy()
        payload.pop("owner_id", None)  
        try:
            updated_place = facade.update_place(place_id, payload)
            return updated_place, 200
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, "Place deleted successfully")
    @api.response(404, "Place not found")
    @api.response(403, "Unauthorized action")
    @api.doc(description="Delete a place by its ID. Owner or admin only.")
    @jwt_required()
    def delete(self, place_id):
        """Delete a place by ID (owner or admin only)"""
        user_id = get_current_user_id()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        if not is_admin and place["owner_id"] != user_id:
            return {"error": "Unauthorized action"}, 403
        try:
            facade.delete_place(place_id)
            return {"message": "Place deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 400
