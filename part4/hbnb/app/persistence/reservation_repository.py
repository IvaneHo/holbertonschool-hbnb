from app.models.reservation import Reservation
from app import db

class ReservationRepository:
    def get(self, res_id):
        return db.session.query(Reservation).get(res_id)

    def get_all(self):
        return db.session.query(Reservation).all()

    def save(self, reservation):
        db.session.add(reservation)
        db.session.commit()
        db.session.refresh(reservation)
        return reservation

    def delete(self, reservation):
        db.session.delete(reservation)
        db.session.commit()

    def exists_conflict(self, place_id, start, end, exclude_res_id=None):
        q = db.session.query(Reservation).filter(
            Reservation.place_id == place_id,
            Reservation.status != "cancelled",
            Reservation.start_date < end,
            Reservation.end_date > start
        )
        if exclude_res_id:
            q = q.filter(Reservation.id != exclude_res_id)
        return db.session.query(q.exists()).scalar()
