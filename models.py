from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BookingCreate(BaseModel):
    name: str
    booking_date: date


class Booking(BookingCreate):
    id: int
    created_at: datetime

    # Gör att Pydantic kan läsa från SQLAlchemy-objekt (attributes)
    model_config = ConfigDict(from_attributes=True)


class BookingUpdate(BaseModel):
    name: Optional[str] = None
    booking_date: Optional[date] = None
