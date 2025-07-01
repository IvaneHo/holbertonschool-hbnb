from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace("reviews", description="Review operations")

# === MODELS ===

review_model = api.model(
    "ReviewInput",
    {
        "text": fields.String(required=True, description="Review text"),
        "rating": fields.Integer(
            required=True, description="Rating from 1 to 5", min=1, max=5
        ),
        "user_id": fields.String(required=True, description="ID of the author"),
        "place_id": fields.String(required=True, description="ID of the place"),
    },
)

review_update_model = api.model(
    "ReviewUpdate",
    {
        "text": fields.String(description="Updated review text"),
        "rating": fields.Integer(
            description="Updated rating from 1 to 5", min=1, max=5
        ),
    },
)

review_response = api.model(
    "ReviewResponse",
    {
        "id": fields.String,
        "text": fields.String,
        "rating": fields.Integer,
        "user_id": fields.String,
        "place_id": fields.String,
        "created_at": fields.String,
        "updated_at": fields.String,
    },
)


@api.route("/")
class ReviewList(Resource):
    @api.marshal_list_with(review_response)
    def get(self):
        """List all reviews"""
        return facade.get_all_reviews()

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_response, code=201)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Create a new review"""
        try:
            return facade.create_review(api.payload), 201
        except Exception as e:
            return {"error": str(e)}, 400


@api.route("/<string:review_id>")
class ReviewItem(Resource):
    # ⚠️ NE PAS mettre @api.marshal_with ici sinon tu as les champs à None quand review absente !
    @api.response(200, "Review retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)
        if not review or not review.get("id"):
            return {"error": "Review not found"}, 404
        return review, 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, "Review updated successfully")
    @api.response(400, "Invalid update data")
    @api.response(404, "Review not found")
    def put(self, review_id):
        """Update review"""
        review_obj = facade.get_review(review_id)
        if not review_obj or not review_obj.get("id"):
            return {"error": "Review not found"}, 404
        try:
            updated = facade.update_review(review_id, api.payload)
            if not updated:
                return {"error": "Review not found"}, 404
            # On renvoie bien l'objet complet mis à jour, mais PAS de marshal_with pour l’erreur
            return facade.get_review(review_id), 200
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, "Review deleted successfully")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """Delete review"""
        review = facade.get_review(review_id)
        if not review or not review.get("id"):
            return {"error": "Review not found"}, 404
        result = facade.delete_review(review_id)
        return result, 200


@api.route("/by_place/<string:place_id>")
class ReviewsByPlace(Resource):
    @api.marshal_list_with(review_response)
    @api.response(200, "List of reviews for the given place retrieved")
    @api.response(404, "Place not found or no reviews")
    def get(self, place_id):
        """Get reviews by place ID"""
        try:
            return facade.get_reviews_by_place(place_id), 200
        except Exception as e:
            return {"error": str(e)}, 404
