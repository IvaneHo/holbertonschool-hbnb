from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

# Namespace pour les utilisateurs
api = Namespace("users", description="User operations")

# Modèle de base pour la création d’un utilisateur (POST)
user_create_model = api.model(
    "UserCreate",
    {
        "first_name": fields.String(required=True, description="First name", default="Jean"),
        "last_name": fields.String(required=True, description="Last name", default="Degolas"),
        "email": fields.String(required=True, description="Email address", default="jean.Degolas@elfesuprme.com"),
        "password": fields.String(required=True, description="User password (min 8 caractères)", min_length=8, default="PAS1233456SVP"),
    },
)

# Modèle complet sans password, utilisé pour PUT/PATCH (update)
user_update_model = api.model(
    "UserUpdate",
    {
        "first_name": fields.String(description="First name"),
        "last_name": fields.String(description="Last name"),
        "email": fields.String(description="Email address"),
        "password": fields.String(description="New password (min 8 caractères)", min_length=8),
    },
)

# Modèle de réponse enrichie (jamais de password)
user_model_response = api.model(
    "UserResponse",
    {
        "id": fields.String(description="User ID"),
        "first_name": fields.String(description="First name"),
        "last_name": fields.String(description="Last name"),
        "email": fields.String(description="Email address"),
        "created_at": fields.String(description="Creation date"),
        "updated_at": fields.String(description="Last update"),
        "is_admin": fields.Boolean(description="Admin status"),
    },
)

@api.route("/")
@api.doc(description="Create a new user or retrieve all users.")
class UserList(Resource):
    @api.expect(user_create_model, validate=True)
    @api.marshal_with(user_model_response)
    @api.response(201, "User successfully created")
    @api.response(400, "Invalid input")
    @api.doc(
        summary="Create user",
        description="Register a new user. Password must be at least 8 characters.",
    )
    def post(self):
        """Register a new user (password required)"""
        try:
            user = facade.create_user(api.payload)
            return user, 201
        except Exception as e:
            api.abort(400, str(e))

    @api.marshal_list_with(user_model_response)
    @api.response(200, "Users retrieved")
    @api.doc(summary="List users", description="Get the list of all registered users.")
    def get(self):
        """Retrieve all users"""
        return facade.get_all_users(), 200

@api.route("/<string:user_id>")
@api.doc(params={"user_id": "The ID of the user"})
class UserResource(Resource):
    @api.marshal_with(user_model_response)
    @api.response(200, "User found")
    @api.response(404, "User not found")
    @api.doc(summary="Get user", description="Retrieve details of a user by their ID.")
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user, 200

    @api.expect(user_update_model, validate=True)
    @api.marshal_with(user_model_response)
    @api.response(200, "User updated")
    @api.response(404, "User not found")
    @api.response(400, "Validation error")
    @api.doc(
        summary="Update user",
        description="Update one or more user fields by ID. (Partial update allowed, including password)",
    )
    def put(self, user_id):
        """Update user by ID (partial update, password allowed)"""
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
    api.models[user_create_model.name] = user_create_model
    api.models[user_update_model.name] = user_update_model
    api.models[user_model_response.name] = user_model_response

