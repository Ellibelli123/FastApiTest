from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime

from database import Base


class BookingEntity(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)  # auto-id i Postgresi
    name = Column(String, nullable=False)
    booking_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
