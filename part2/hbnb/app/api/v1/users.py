from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Modèle complet requis pour POST (création)
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
})

# Modèle partiel autorisé pour PUT (modification)
user_partial_model = api.model('UserPartial', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
})

# Réponse enrichie
user_model_response = api.inherit('UserResponse', user_model, {
    'id': fields.String(description='User ID'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update'),
    'is_admin': fields.Boolean(description='Admin status'),
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input')
    def post(self):
        """Register a new user"""
        try:
            user = facade.create_user(api.payload)
            return user, 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Users retrieved')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        return api.marshal(users, user_model_response), 200


@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User found')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return api.marshal(user, user_model_response), 200

    @api.expect(user_partial_model, validate=True)
    @api.response(200, 'User updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Validation error')
    def put(self, user_id):
        """Update user by ID (partial update allowed)"""
        try:
            user = facade.update_user(user_id, api.payload)
            if not user:
                return {'error': 'User not found'}, 404
            return api.marshal(user, user_model_response), 200
        except Exception as e:
            return {'error': str(e)}, 400
