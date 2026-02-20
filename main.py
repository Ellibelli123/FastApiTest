from datetime import date, datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})


class BookingCreate(BaseModel):
    name: str
    class_id: int
    pass_date: date


class Booking(BookingCreate):
    id: int
    created_at: datetime


class BookingUpdate(BaseModel):
    name: Optional[str] = None
    class_id: Optional[int] = None
    pass_date: Optional[date] = None



bookings: list[Booking] = []


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Hello FastAPI"}


@app.get("/magnus")
def read_magnus():
    return {"status": "ok", "message": "Magnus Hello FastAPI"}


@app.get("/bookings", response_model=list[Booking])
def list_bookings():
    return bookings



@app.post("/bookings", response_model=Booking)
def create_booking(
    name: str = Form(...),
    class_id: int = Form(...),
    pass_date: date = Form(...),
):
    payload = BookingCreate(name=name, class_id=class_id, pass_date=pass_date)

    booking = Booking(
        id=len(bookings) + 1,
        name=payload.name,
        class_id=payload.class_id,
        pass_date=payload.pass_date,
        created_at=datetime.now(),
    )
    bookings.append(booking)
    return booking



@app.put("/bookings/{booking_id}", response_model=Booking)
def update_booking(
    booking_id: int,
    name: str = Form(...),
    class_id: int = Form(...),
    pass_date: date = Form(...),
):
    payload = BookingCreate(name=name, class_id=class_id, pass_date=pass_date)

    for booking in bookings:
        if booking.id == booking_id:
            booking.name = payload.name
            booking.class_id = payload.class_id
            booking.pass_date = payload.pass_date
            return booking

    raise HTTPException(status_code=404, detail="Booking not found")



@app.patch("/bookings/{booking_id}", response_model=Booking)
def patch_booking(
    booking_id: int,
    name: Optional[str] = Form(None),
    class_id: Optional[int] = Form(None),
    pass_date: Optional[date] = Form(None),
):
    payload = BookingUpdate(name=name, class_id=class_id, pass_date=pass_date)

    for booking in bookings:
        if booking.id == booking_id:
            if payload.name is not None:
                booking.name = payload.name
            if payload.class_id is not None:
                booking.class_id = payload.class_id
            if payload.pass_date is not None:
                booking.pass_date = payload.pass_date
            return booking

    raise HTTPException(status_code=404, detail="Booking not found")