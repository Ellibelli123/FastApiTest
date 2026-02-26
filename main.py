from datetime import date
from typing import Optional

from fastapi import FastAPI, HTTPException, Form, Depends, Body
from sqlalchemy.orm import Session

import booking_service as svc
from database import Base, engine, get_db
from models import Booking

from services.faq_handler import FaqHandler
from pydantic import BaseModel
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

Base.metadata.create_all(bind=engine)


@app.get("/bookings", response_model=list[Booking])
def list_bookings(db: Session = Depends(get_db)):
    return svc.list_bookings(db)


@app.get("/bookings/{booking_id}", response_model=Booking)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = svc.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@app.post("/bookings", response_model=Booking)
def create_booking(
        name: str = Form(..., description="Enter name"),
        booking_date: date = Form(..., description="Enter booking date"),
        db: Session = Depends(get_db),
):
    return svc.create_booking(db, name=name, booking_date=booking_date)


@app.put("/bookings/{booking_id}", response_model=Booking)
def update_booking_put(
        booking_id: int,
        name: str = Form(..., description="Enter name"),
        booking_date: date = Form(..., description="Enter booking date"),
        db: Session = Depends(get_db),
):
    booking = svc.update_booking_put(db, booking_id, name, booking_date)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@app.patch("/bookings/{booking_id}", response_model=Booking)
def update_booking_patch(
        booking_id: int,
        name: Optional[str] = Form(None),
        booking_date: Optional[date] = Form(None),
        db: Session = Depends(get_db),
):
    booking = svc.update_booking_patch(db, booking_id, name=name, booking_date=booking_date)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    ok = svc.delete_booking(db, booking_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"status": "ok", "message": "Booking deleted"}


faq_handler = FaqHandler()

class FaqRequest(BaseModel):
    question: str

class FaqResponse(BaseModel):
    question: str
    answer: str | None

@app.post("/faq", response_model=FaqResponse)
async def ask_faq(req: FaqRequest):
    answer = await faq_handler.get_answer(req.question)
    return {"question": req.question, "answer": answer}