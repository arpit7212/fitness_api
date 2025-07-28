from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Slot
import pytz

router = APIRouter()

@router.put("/slots/{slot_id}/change_timezone/")
def change_timezone(slot_id: int, new_timezone: str, db: Session = Depends(get_db)):
    # Validate timezone
    try:
        new_tz = pytz.timezone(new_timezone)
    except pytz.UnknownTimeZoneError:
        raise HTTPException(status_code=400, detail="Invalid timezone")

    # Get target slot
    target_slot = db.query(Slot).filter(Slot.id == slot_id).first()
    if not target_slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    subject_id = target_slot.subject_id

    # Fetch all slots for that subject
    slots = db.query(Slot).filter(Slot.subject_id == subject_id).all()

    for slot in slots:
        # Assume old datetimes are in UTC if naive (no tzinfo)
        if slot.start_time.tzinfo is None:
            old_start = pytz.utc.localize(slot.start_time)
        else:
            old_start = slot.start_time

        if slot.end_time.tzinfo is None:
            old_end = pytz.utc.localize(slot.end_time)
        else:
            old_end = slot.end_time

        # Convert from UTC → new timezone
        new_start = old_start.astimezone(new_tz)
        new_end = old_end.astimezone(new_tz)

        # Save new timezone-aware datetime
        slot.start_time = new_start
        slot.end_time = new_end

    db.commit()

    return {"detail": f"All slots for subject {subject_id} updated to timezone '{new_timezone}'"}


