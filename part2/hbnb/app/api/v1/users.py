from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Modèle de base pour création
user_model_base = api.model('UserBase', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
})

# Modèle pour affichage complet
user_model = api.inherit('User', user_model_base, {})

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
@api.doc(description="Create a new user or retrieve all users.")
class UserList(Resource):
    @api.expect(user_model_base, validate=True)
    @api.marshal_with(user_model_response)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input')
    @api.doc(summary="Create user", description="Create a new user with first name, last name, and email.")
    def post(self):
        """Register a new user"""
        try:
            user = facade.create_user(api.payload)
            return user, 201
        except Exception as e:
            api.abort(400, str(e))

    @api.marshal_list_with(user_model_response)
    @api.response(200, 'Users retrieved')
    @api.doc(summary="List users", description="Get the list of all registered users.")
    def get(self):
        """Retrieve all users"""
        return facade.get_all_users(), 200


@api.route('/<string:user_id>')
@api.doc(params={'user_id': 'The ID of the user'})
class UserResource(Resource):
    @api.marshal_with(user_model_response)
    @api.response(200, 'User found')
    @api.response(404, 'User not found')
    @api.doc(summary="Get user", description="Retrieve details of a user by their ID.")
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user, 200

    @api.expect(user_partial_model, validate=True)
    @api.marshal_with(user_model_response)
    @api.response(200, 'User updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Validation error')
    @api.doc(summary="Update user", description="Update one or more user fields by ID (partial update allowed).")
    def put(self, user_id):
        """Update user by ID (partial update allowed)"""
        user_exists = facade.get_user(user_id)
        if not user_exists:
            api.abort(404, "User not found")
        try:
            user = facade.update_user(user_id, api.payload)
            return user, 200
        except Exception as e:
            api.abort(400, str(e))


def register_user_models(api):
    """Force l'enregistrement Swagger des modèles utilisateurs"""
    api.models[user_model_base.name] = user_model_base
    api.models[user_model.name] = user_model
    api.models[user_partial_model.name] = user_partial_model
    api.models[user_model_response.name] = user_model_response

