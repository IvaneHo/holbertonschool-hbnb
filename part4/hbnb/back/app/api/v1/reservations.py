from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade
from app.schemas.reservation import ReservationCreateSchema, ReservationUpdateSchema

api = Namespace("reservations", description="Reservations operations")

def get_current_user_id():
    ident = get_jwt_identity()
    return ident if isinstance(ident, str) else ident.get("id")

# MODELS SWAGGER

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
        "status": fields.String(description="Status (pending/approved/rejected/cancelled)", required=False),
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

error_model = api.model(
    "Error",
    {"error": fields.String(description="Error message")}
)

# ROUTES

@api.route("/")
class ReservationListResource(Resource):
    @api.marshal_list_with(reservation_response_model)
    @jwt_required()
    def get(self):
        """Retrieve reservations (all if admin, only yours if user)"""
        user_id = get_current_user_id()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if is_admin:
            return facade.get_all_reservations(), 200
        all_res = facade.get_all_reservations()
        my_res = [r for r in all_res if r["user_id"] == user_id]
        return my_res, 200

    @api.expect(reservation_model, validate=True)
    @api.response(201, "Reservation created", reservation_response_model)
    @api.response(400, "Bad Request", error_model)
    @api.response(403, "Permission Denied", error_model)
    @jwt_required()
    def post(self):
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
    @api.response(200, "Reservation found", reservation_response_model)
    @api.response(404, "Reservation not found", error_model)
    @jwt_required()
    def get(self, res_id):
        """Get a reservation by ID"""
        res = facade.get_reservation(res_id)
        if not res:
            return {"error": "Reservation not found"}, 404
        return res, 200

    @api.expect(reservation_update_model, validate=True)
    @api.response(200, "Reservation updated", reservation_response_model)
    @api.response(400, "Bad Request", error_model)
    @api.response(403, "Permission Denied", error_model)
    @api.response(404, "Reservation not found", error_model)
    @jwt_required()
    def put(self, res_id):
        """Update a reservation (only owner/admin can validate/reject, user can cancel)"""
        try:
            data = ReservationUpdateSchema(**api.payload).model_dump()
        except Exception as e:
            return {"error": str(e)}, 400

        user_id = get_current_user_id()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        reservation = facade.get_reservation(res_id)
        if not reservation:
            return {"error": "Reservation not found"}, 404

        # Autorisation sur la modification du statut
        if "status" in data and data["status"] and data["status"] != reservation["status"]:
            if data["status"] == "cancelled":
                # Annulation par le propriétaire de la réservation
                if reservation["user_id"] != user_id:
                    return {"error": "You can only cancel your own reservations."}, 403
            elif data["status"] in ("approved", "rejected"):
                # Seul owner de la place ou admin peut valider/rejeter
                place = facade.get_place(reservation["place_id"])
                if not place:
                    return {"error": "Associated place not found"}, 404
                if not (is_admin or place.get("owner_id") == user_id):
                    return {"error": "Only the place owner or admin can approve/reject a reservation."}, 403
            elif data["status"] not in ("pending", "approved", "rejected", "cancelled"):
                return {"error": "Invalid status value."}, 400

        try:
            updated = facade.update_reservation(res_id, data)
            if not updated:
                return {"error": "Reservation not found"}, 404
            return updated, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, "Reservation deleted")
    @api.response(404, "Reservation not found", error_model)
    @api.response(403, "Permission Denied", error_model)
    @jwt_required()
    def delete(self, res_id):
        """Delete a reservation (only owner or admin)"""
        user_id = get_current_user_id()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        reservation = facade.get_reservation(res_id)
        if not reservation:
            return {"error": "Reservation not found"}, 404

        # Seul le créateur ou l'admin peut supprimer
        if not (is_admin or reservation["user_id"] == user_id):
            return {"error": "Only the reservation owner or an admin can delete this reservation."}, 403

        deleted = facade.delete_reservation(res_id)
        if not deleted:
            return {"error": "Reservation not found"}, 404
        return {"message": "Reservation deleted."}, 200
