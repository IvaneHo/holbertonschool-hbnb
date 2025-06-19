from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('places', description='Place operations')

# === MODELS ===
place_model = api.model('Place', {
    'title': fields.String(required=True, description="Title of the place"),
    'description': fields.String(description="Description of the place"),
    'price': fields.Float(required=True, description="Price per night (non-negative)"),
    'latitude': fields.Float(required=True, description="Latitude between -90 and 90"),
    'longitude': fields.Float(required=True, description="Longitude between -180 and 180"),
    'owner_id': fields.String(required=True, description="User ID of the place owner"),
    'amenities': fields.List(fields.String, required=True, description="List of Amenity IDs")
})

# === ROUTES ===
@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc(description="Create a new place with validated attributes and related entities")
    def post(self):
        """Create a new place"""
        try:
            return facade.create_place(api.payload), 201
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of all places retrieved')
    @api.doc(description="Retrieve the full list of places (with coordinates and titles)")
    def get(self):
        """Retrieve all places"""
        return facade.get_all_places(), 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place retrieved successfully')
    @api.response(404, 'Place not found')
    @api.doc(description="Get a place by its ID, including its amenities and owner details")
    def get(self, place_id):
        """Get a place by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    @api.response(400, 'Validation error')
    @api.doc(description="Update all details of a place by its ID")
    def put(self, place_id):
        """Update a place by ID"""
        try:
            result = facade.update_place(place_id, api.payload)
            if not result:
                return {"error": "Place not found"}, 404
            return result, 200
        except Exception as e:
            return {"error": str(e)}, 400
