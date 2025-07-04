from flask_restx import Namespace, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

# Namespace pour les utilisateurs
api = Namespace("users", description="User operations")

user_create_model = api.model(
    "UserCreate",
    {
        "first_name": fields.String(required=True, description="First name", default="Jean"),
        "last_name": fields.String(required=True, description="Last name", default="Degolas"),
        "email": fields.String(required=True, description="Email address", default="jean.Degolas@elfesuprme.com"),
        "password": fields.String(required=True, description="User password (min 8 caractères)", min_length=8, default="PAS1233456SVP"),
    },
)

user_update_model = api.model(
    "UserUpdate",
    {
        "first_name": fields.String(description="First name"),
        "last_name": fields.String(description="Last name"),
        "email": fields.String(description="Email address"),  # Interdit par la logique
        "password": fields.String(description="New password (min 8 caractères)", min_length=8),  # Interdit aussi
    },
)

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
class UserList(Resource):
    @api.expect(user_create_model, validate=True)
    @api.marshal_with(user_model_response)
    @api.response(201, "User successfully created")
    @api.response(400, "Invalid input")
    def post(self):
        """Register a new user (password required)"""
        try:
            user = facade.create_user(api.payload)
            return user, 201
        except Exception as e:
            api.abort(400, str(e))

    @api.marshal_list_with(user_model_response)
    @api.response(200, "Users retrieved")
    def get(self):
        """Retrieve all users"""
        return facade.get_all_users(), 200

@api.route("/<string:user_id>")
@api.doc(params={"user_id": "The ID of the user"})
class UserResource(Resource):
    @api.marshal_with(user_model_response)
    @api.response(200, "User found")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        return user, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, "User updated")
    @api.response(404, "User not found")
    @api.response(400, "Validation error")
    @api.response(403, "Unauthorized action")
    @jwt_required()
    def put(self, user_id):
        """
        Update user by ID (user only, can't change email or password)
        """
        jwt_user = get_jwt_identity()
        if isinstance(jwt_user, dict):
            jwt_user = jwt_user.get("id")
        if user_id != jwt_user:
            return {"error": "Unauthorized action"}, 403

        payload = api.payload.copy()
        if "email" in payload or "password" in payload:
            return {"error": "You cannot modify email or password"}, 400

        user_exists = facade.get_user(user_id)
        if not user_exists:
            return {"error": "User not found"}, 404
        try:
            user = facade.update_user(user_id, payload)
            # Marshal uniquement en cas de succès
            return marshal(user, user_model_response), 200
        except Exception as e:
            return {"error": str(e)}, 400

    @api.expect(user_update_model, validate=True)
    @api.response(200, "User updated (PATCH)")
    @api.response(404, "User not found")
    @api.response(400, "Validation error")
    @api.response(403, "Unauthorized action")
    @jwt_required()
    def patch(self, user_id):
        """
        Patch user by ID (user only, can't change email or password)
        """
        jwt_user = get_jwt_identity()
        if isinstance(jwt_user, dict):
            jwt_user = jwt_user.get("id")
        if user_id != jwt_user:
            return {"error": "Unauthorized action"}, 403

        payload = api.payload.copy()
        if "email" in payload or "password" in payload:
            return {"error": "You cannot modify email or password"}, 400

        user_exists = facade.get_user(user_id)
        if not user_exists:
            return {"error": "User not found"}, 404
        try:
            user = facade.update_user(user_id, payload)
            return marshal(user, user_model_response), 200
        except Exception as e:
            return {"error": str(e)}, 400

def register_user_models(api):
    """Force l'enregistrement Swagger des modèles utilisateurs"""
    api.models[user_create_model.name] = user_create_model
    api.models[user_update_model.name] = user_update_model
    api.models[user_model_response.name] = user_model_response
