from datetime import datetime
from typing import List, Optional

from models import Booking, BookingCreate, BookingUpdate

bookings: List[Booking] = []
_next_id: int = 1


def list_bookings() -> List[Booking]:
    return bookings


def get_booking(booking_id: int) -> Optional[Booking]:
    for b in bookings:
        if b.id == booking_id:
            return b
    return None


def create_booking(payload: BookingCreate) -> Booking:
    global _next_id

    booking = Booking(
        id=_next_id,
        name=payload.name,
        booking_date=payload.booking_date,
        created_at=datetime.now(),
    )
    _next_id += 1
    bookings.append(booking)
    return booking


def update_booking_put(booking_id: int, payload: BookingCreate) -> Optional[Booking]:
    booking = get_booking(booking_id)
    if not booking:
        return None

    booking.name = payload.name
    booking.booking_date = payload.booking_date
    return booking


def update_booking_patch(booking_id: int, payload: BookingUpdate) -> Optional[Booking]:
    booking = get_booking(booking_id)
    if not booking:
        return None

    if payload.name is not None:
        booking.name = payload.name
    if payload.booking_date is not None:
        booking.booking_date = payload.booking_date

    return booking
