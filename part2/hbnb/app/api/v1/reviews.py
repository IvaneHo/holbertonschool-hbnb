from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

# Namespace pour les opérations liées aux reviews (avis)
api = Namespace('reviews', description='Review operations')

# === MODELS ===

# Modèle pour la création d’un avis (requête POST)
review_model = api.model('ReviewInput', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5',
                             min=1, max=5),
    'user_id': fields.String(required=True, description='ID of the author'),
    'place_id': fields.String(required=True, description='ID of the place'),
})

# Modèle pour la mise à jour d’un avis (requête PUT)
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Updated review text'),
    'rating': fields.Integer(description='Updated rating from 1 to 5',
                             min=1, max=5),
})

# Modèle pour les réponses envoyées à l’utilisateur
review_response = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating'),
    'user_id': fields.String(description='User ID'),
    'place_id': fields.String(description='Place ID'),
    'created_at': fields.String(description='Created date'),
    'updated_at': fields.String(description='Updated date'),
})

# === ROUTES ===


@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_response)
    @api.response(200, 'List of all reviews retrieved')
    @api.doc(description="Retrieve the list of all reviews in the system")
    def get(self):
        """List all reviews"""
        # Retourne toutes les reviews enregistrées
        return facade.get_all_reviews()

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_response, code=201)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc(description="Create a new review for a given place and user")
    def post(self):
        """Create a new review"""
        # Crée une nouvelle review à partir des données envoyées
        try:
            return facade.create_review(api.payload), 201
        except Exception as e:
            # Retourne une erreur 400 si les données sont invalides
            return {'error': str(e)}, 400


@api.route('/<string:review_id>')
@api.doc(params={"review_id": "ID of the review"})
class ReviewItem(Resource):
    @api.marshal_with(review_response)
    @api.response(200, 'Review retrieved successfully')
    @api.response(404, 'Review not found')
    @api.doc(description="Get a review by its ID")
    def get(self, review_id):
        """Get review by ID"""
        # Récupère une review en fonction de son ID
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review

    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid update data')
    @api.response(404, 'Review not found')
    @api.doc(description="Update an existing review by ID")
    def put(self, review_id):
        """Update review"""
        # Met à jour une review existante
        try:
            updated = facade.update_review(review_id, api.payload)
            if not updated:
                return {'error': 'Review not found'}, 404
            return facade.get_review(review_id), 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.doc(description="Delete a review by its ID")
    def delete(self, review_id):
        """Delete review"""
        # Supprime une review via son ID
        result = facade.delete_review(review_id)
        if not result:
            return {'error': 'Review not found'}, 404
        return result


@api.route('/by_place/<string:place_id>')
@api.doc(params={"place_id": "ID of the place"})
class ReviewsByPlace(Resource):
    @api.marshal_list_with(review_response)
    @api.response(200, 'List of reviews for the given place retrieved')
    @api.response(404, 'Place not found or no reviews')
    def get(self, place_id):
        """Get reviews by place ID"""
        # Récupère les reviews associées à un lieu donné
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        return reviews, 200
