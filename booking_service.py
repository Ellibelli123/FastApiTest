from typing import Optional, List

from sqlalchemy.orm import Session

from booking_entity import BookingEntity


def list_bookings(db: Session) -> List[BookingEntity]:
    return db.query(BookingEntity).all()


def create_booking(db: Session, name: str, booking_date):
    booking = BookingEntity(name=name, booking_date=booking_date)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_booking(db: Session, booking_id: int) -> Optional[BookingEntity]:
    return db.query(BookingEntity).filter(BookingEntity.id == booking_id).first()


def update_booking_put(db: Session, booking_id: int, name: str, booking_date):
    booking = get_booking(db, booking_id)
    if not booking:
        return None

    booking.name = name
    booking.booking_date = booking_date
    db.commit()
    db.refresh(booking)
    return booking


def update_booking_patch(db: Session, booking_id: int, name=None, booking_date=None):
    booking = get_booking(db, booking_id)
    if not booking:
        return None

    if name is not None:
        booking.name = name
    if booking_date is not None:
        booking.booking_date = booking_date

    db.commit()
    db.refresh(booking)
    return booking


def delete_booking(db: Session, booking_id: int) -> bool:
    booking = get_booking(db, booking_id)
    if not booking:
        return False

    db.delete(booking)
    db.commit()
    return True
