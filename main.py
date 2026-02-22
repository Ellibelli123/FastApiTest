from datetime import date, datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, Form
from pydantic import BaseModel

from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db, Base, engine
from models import BookingEntity

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})


Base.metadata.create_all(bind=engine)



class BookingCreate(BaseModel):
    name: str
    class_id: int
    pass_date: date


class BookingUpdate(BaseModel):
    name: Optional[str] = None
    class_id: Optional[int] = None
    pass_date: Optional[date] = None


class BookingResponse(BaseModel):
    id: int
    name: str
    class_id: int
    pass_date: date
    created_at: datetime

    class Config:
        from_attributes = True  # behövs för SQLAlchemy -> Pydantic



@app.get("/")
def root():
    return {"status": "ok", "message": "Hello FastAPI"}


@app.get("/magnus")
def magnus():
    return {"status": "ok", "message": "Magnus Hello FastAPI"}


@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    version = db.execute(text("SELECT version();")).fetchone()[0]
    return {"database": version}


@app.get("/bookings", response_model=list[BookingResponse])
def list_bookings(db: Session = Depends(get_db)):
    return db.query(BookingEntity).order_by(BookingEntity.id.asc()).all()


@app.post("/bookings", response_model=BookingResponse)
def create_booking(
    name: str = Form(...),
    class_id: int = Form(...),
    pass_date: date = Form(...),
    db: Session = Depends(get_db),
):
    booking = BookingEntity(name=name, class_id=class_id, pass_date=pass_date)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@app.put("/bookings/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int,
    name: str = Form(...),
    class_id: int = Form(...),
    pass_date: date = Form(...),
    db: Session = Depends(get_db),
):
    booking = db.query(BookingEntity).filter(BookingEntity.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.name = name
    booking.class_id = class_id
    booking.pass_date = pass_date

    db.commit()
    db.refresh(booking)
    return booking


@app.patch("/bookings/{booking_id}", response_model=BookingResponse)
def patch_booking(
    booking_id: int,
    name: Optional[str] = Form(None),
    class_id: Optional[int] = Form(None),
    pass_date: Optional[date] = Form(None),
    db: Session = Depends(get_db),
):
    booking = db.query(BookingEntity).filter(BookingEntity.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if name is not None:
        booking.name = name
    if class_id is not None:
        booking.class_id = class_id
    if pass_date is not None:
        booking.pass_date = pass_date

    db.commit()
    db.refresh(booking)
    return booking