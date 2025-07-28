from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, crud

router = APIRouter()


@router.post("/slots/")
def create_slot(slot: schemas.SlotCreate, db: Session = Depends(get_db)):
    return crud.create_slot(db, slot)

@router.post("/bookings/")
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_booking(db, booking)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/slots/", response_model=list[schemas.Slot])
def read_slots(db: Session = Depends(get_db)):
    return db.query(models.Slot).all()

@router.get("/bookings/")
def read_bookings(db: Session = Depends(get_db)):
    return db.query(models.Booking).all()