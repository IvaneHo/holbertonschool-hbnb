from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace("protected", description="JWT protected endpoint")

@api.route("/")
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()   
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        return {
            "message": "JWT valide !",
            "user_id": user_id,
            "is_admin": is_admin
        }, 200
