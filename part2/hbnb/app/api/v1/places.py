from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String, required=True)
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created')
    def post(self):
        try:
            return facade.create_place(api.payload), 201
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'All places returned')
    def get(self):
        return facade.get_all_places(), 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place returned')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated')
    @api.response(404, 'Place not found')
    def put(self, place_id):
        try:
            result = facade.update_place(place_id, api.payload)
            if not result:
                return {"error": "Place not found"}, 404
            return result, 200
        except Exception as e:
            return {"error": str(e)}, 400
