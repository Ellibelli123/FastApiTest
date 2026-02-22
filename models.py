from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func

from database import Base


class BookingEntity(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    class_id = Column(Integer, nullable=False)
    pass_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)