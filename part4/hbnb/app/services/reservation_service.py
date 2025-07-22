from app.models.reservation import Reservation
from app.persistence.reservation_repository import ReservationRepository
from app.models.place import Place
from app.schemas.reservation import ReservationResponseSchema
import uuid

class ReservationService:
    def __init__(self):
        self.repo = ReservationRepository()

    def create_reservation(self, user_id, data):
        place_id = data['place_id']
        start = data['start_date']
        end = data['end_date']

        place = Place.query.get(place_id)
        if not place:
            raise ValueError("Logement introuvable.")
        if place.owner_id == user_id:
            raise PermissionError("Vous ne pouvez pas réserver votre propre logement.")
        if self.repo.exists_conflict(place_id, start, end):
            raise ValueError("Ce logement est déjà réservé sur cette période.")

        reservation = Reservation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            place_id=place_id,
            start_date=start,
            end_date=end,
            status='pending'
        )
        self.repo.save(reservation)
        return ReservationResponseSchema.from_orm_reservation(reservation).model_dump(mode="json")

    def get_reservation(self, res_id):
        reservation = self.repo.get(res_id)
        if not reservation:
            return None
        return ReservationResponseSchema.from_orm_reservation(reservation).model_dump(mode="json")

    def get_all_reservations(self):
        reservations = self.repo.get_all()
        return [ReservationResponseSchema.from_orm_reservation(r).model_dump(mode="json") for r in reservations]

    def update_reservation(self, res_id, data):
        reservation = self.repo.get(res_id)
        if not reservation:
            return None
        if 'start_date' in data and data['start_date']:
            reservation.start_date = data['start_date']
        if 'end_date' in data and data['end_date']:
            reservation.end_date = data['end_date']
        if 'status' in data and data['status']:
            reservation.status = data['status']
        self.repo.save(reservation)
        return ReservationResponseSchema.from_orm_reservation(reservation).model_dump(mode="json")

    def delete_reservation(self, res_id):
        reservation = self.repo.get(res_id)
        if not reservation:
            return False
        self.repo.delete(reservation)
        return True
