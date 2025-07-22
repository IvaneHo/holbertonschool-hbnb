from app.models.reservation import Reservation
from app.persistence.reservation_repository import ReservationRepository
from app.models.place import Place
from app.schemas.reservation import ReservationResponseSchema
from datetime import datetime

class ReservationService:
    def __init__(self):
        self.repo = ReservationRepository()  # <-- C'est ce qu'il manquait !

    def create_reservation(self, user_id, data):
        # Conversion des dates si besoin
        if isinstance(data['start_date'], str):
            data['start_date'] = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
        if isinstance(data['end_date'], str):
            data['end_date'] = datetime.strptime(data['end_date'], "%Y-%m-%d").date()

        reservation = Reservation(
            user_id=user_id,
            place_id=data['place_id'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            status='pending'
        )
        self.repo.save(reservation)
        return ReservationResponseSchema(
            id=reservation.id,
            user_id=reservation.user_id,
            place_id=reservation.place_id,
            start_date=reservation.start_date,
            end_date=reservation.end_date,
            status=reservation.status,
            created_at=str(reservation.created_at),
            updated_at=str(reservation.updated_at)
        ).model_dump(mode="json")

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
            if isinstance(data['start_date'], str):
                data['start_date'] = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
            reservation.start_date = data['start_date']
        if 'end_date' in data and data['end_date']:
            if isinstance(data['end_date'], str):
                data['end_date'] = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
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
