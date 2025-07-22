from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade  # <-- On importe facade, pas ReservationService direct !
from app.schemas.reservation import ReservationCreateSchema, ReservationUpdateSchema

api = Namespace("reservations", description="Reservations operations")

def get_current_user_id():
    ident = get_jwt_identity()
    return ident if isinstance(ident, str) else ident.get("id")

# --- MODELS SWAGGER (pour formulaire/documentation Swagger) ---

reservation_model = api.model(
    "ReservationCreate",
    {
        "place_id": fields.String(required=True, description="ID of the place"),
        "start_date": fields.String(required=True, description="Start date (YYYY-MM-DD)"),
        "end_date": fields.String(required=True, description="End date (YYYY-MM-DD)"),
    }
)

reservation_update_model = api.model(
    "ReservationUpdate",
    {
        "start_date": fields.String(description="Start date (YYYY-MM-DD)"),
        "end_date": fields.String(description="End date (YYYY-MM-DD)"),
        "status": fields.String(description="Status (pending/approved/cancelled)", required=False),
    }
)

reservation_response_model = api.model(
    "ReservationResponse",
    {
        "id": fields.String(description="Reservation ID"),
        "user_id": fields.String(description="ID of the user"),
        "place_id": fields.String(description="ID of the place"),
        "start_date": fields.String(description="Start date"),
        "end_date": fields.String(description="End date"),
        "status": fields.String(description="Reservation status"),
        "created_at": fields.String(description="Creation timestamp"),
        "updated_at": fields.String(description="Last update timestamp"),
    }
)

# --- ROUTES ---

@api.route("/")
class ReservationListResource(Resource):
    @api.marshal_list_with(reservation_response_model)
    @jwt_required()
    def get(self):
        """Retrieve all reservations"""
        return facade.get_all_reservations(), 200

    @api.expect(reservation_model, validate=True)
    @api.marshal_with(reservation_response_model, code=201)
    @jwt_required()
    def post(self):
        """Create a reservation"""
        try:
            payload = api.payload or {}
            data = ReservationCreateSchema(**payload).model_dump()
        except Exception as e:
            return {"error": f"Invalid input: {e}"}, 400

        user_id = get_current_user_id()
        try:
            res = facade.create_reservation(user_id, data)
            return res, 201
        except PermissionError as e:
            return {"error": str(e)}, 403
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"Unexpected error: {e}"}, 400

@api.route("/<string:res_id>")
class ReservationResource(Resource):
    @api.marshal_with(reservation_response_model)
    @jwt_required()
    def get(self, res_id):
        """Get a reservation by ID"""
        res = facade.get_reservation(res_id)
        if not res:
            return {"error": "Reservation not found"}, 404
        return res, 200

    @api.expect(reservation_update_model, validate=True)
    @api.marshal_with(reservation_response_model)
    @jwt_required()
    def put(self, res_id):
        """Update a reservation"""
        try:
            data = ReservationUpdateSchema(**api.payload).model_dump()
        except Exception as e:
            return {"error": str(e)}, 400
        try:
            updated = facade.update_reservation(res_id, data)
            if not updated:
                return {"error": "Reservation not found"}, 404
            return updated, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()
    def delete(self, res_id):
        """Delete a reservation"""
        deleted = facade.delete_reservation(res_id)
        if not deleted:
            return {"error": "Reservation not found"}, 404
        return {"message": "Reservation deleted."}, 200
