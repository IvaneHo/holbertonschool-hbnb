from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace("reviews", description="Review operations")

def get_current_user_id():
    ident = get_jwt_identity()
    return ident if isinstance(ident, str) else ident.get("id")

review_model = api.model(
    "ReviewInput",
    {
        "text": fields.String(required=True, description="Review text"),
        "rating": fields.Integer(required=True, description="Rating from 1 to 5", min=1, max=5),
        "place_id": fields.String(required=True, description="ID of the place"),
    },
)

review_update_model = api.model(
    "ReviewUpdate",
    {
        "text": fields.String(description="Updated review text"),
        "rating": fields.Integer(description="Updated rating from 1 to 5", min=1, max=5),
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
        """List all reviews (public)"""
        return facade.get_all_reviews()

    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @jwt_required()
    def post(self):
        """Create a new review (auth, not on own place, not twice)"""
        user_id = get_current_user_id()
        data = api.payload.copy()
        data["user_id"] = user_id

        place = facade.get_place(data["place_id"])
        if not place:
            return {"error": "Place not found"}, 400
        if getattr(place, "owner_id", None) == user_id:
            return {"error": "You cannot review your own place"}, 400

        all_reviews = facade.get_reviews_by_place(data["place_id"])
        for review in all_reviews:
            user_id_cmp = review.get("user_id")
            if not user_id_cmp:
                continue  
            if user_id_cmp == user_id:
                return {"error": "You have already reviewed this place"}, 400

        try:
            result = facade.create_review(data)
            if not result or not result.get("id"):
               return {"error": "Internal server error: Review not created"}, 500
            return result, 201
        except Exception as e:
            return {"error": str(e)}, 400

@api.route("/<string:review_id>")
class ReviewItem(Resource):
    @api.marshal_with(review_response)
    @api.response(200, "Review retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Get review by ID (public)"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review, 200

    @api.expect(review_update_model, validate=True)
    @api.marshal_with(review_response)
    @api.response(200, "Review updated successfully")
    @api.response(400, "Invalid update data")
    @api.response(404, "Review not found")
    @api.response(403, "Unauthorized action")
    @jwt_required()
    def put(self, review_id):
        """Update review (owner OR admin)"""
        user_id = get_current_user_id()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        if not is_admin and review["user_id"] != user_id:
            return {"error": "Unauthorized action"}, 403

        try:
            updated = facade.update_review(review_id, api.payload)
            return updated, 200
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, "Review deleted successfully")
    @api.response(404, "Review not found")
    @api.response(403, "Unauthorized action")
    @jwt_required()
    def delete(self, review_id):
        """Delete review (owner OR admin)"""
        user_id = get_current_user_id()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        if not is_admin and review["user_id"] != user_id:
            return {"error": "Unauthorized action"}, 403
        try:
            result = facade.delete_review(review_id)
            return result, 200
        except Exception as e:
            return {"error": str(e)}, 400

@api.route("/by_place/<string:place_id>")
class ReviewsByPlace(Resource):
    @api.marshal_list_with(review_response)
    @api.response(200, "List of reviews for the given place retrieved")
    @api.response(404, "Place not found or no reviews")
    def get(self, place_id):
        """Get reviews by place ID (public)"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return reviews, 200
        except Exception as e:
            return {"error": str(e)}, 404
