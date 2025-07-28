# crud.py
from sqlalchemy.orm import Session
from app.models import Subject, Client, Slot, Booking
from app.schemas import SubjectCreate, ClientCreate, SlotCreate, BookingCreate, SlotInfo
from sqlalchemy import and_
from datetime import datetime
import pytz

def create_subject(db: Session, subject: SubjectCreate):
    # Create and store a new subject with timezone
    db_subject = Subject(name=subject.name, instructor=subject.instructor, timezone=subject.timezone)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def create_client(db: Session, client: ClientCreate):
    # Create and store a new client
    db_client = Client(name=client.name)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def create_slot(db: Session, slot: SlotCreate):
    # Fetch subject to determine its timezone
    subject = db.query(Subject).filter(Subject.id == slot.subject_id).first()
    if not subject:
        raise Exception("Subject not found")

    # Convert slot times from subject's timezone to UTC
    tz = pytz.timezone(subject.timezone)

    #start = tz.localize(slot.start_time)
    #end = tz.localize(slot.end_time)
    
    if slot.start_time.tzinfo is None:
        start = tz.localize(slot.start_time)
    else:
        start = slot.start_time.astimezone(tz)
    
    if slot.end_time.tzinfo is None:
        end = tz.localize(slot.start_time)
    else:
        end = slot.end_time.astimezone(tz)
    

    # Store times in UTC for consistency
    db_slot = Slot(
        subject_id=slot.subject_id,
        start_time=start.astimezone(pytz.UTC),
        end_time=end.astimezone(pytz.UTC),
    )
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

def create_booking(db: Session, booking: BookingCreate):
    # Fetch client and slot by IDs
    client = db.query(Client).filter(Client.id == booking.client_id).first()
    slot = db.query(Slot).filter(Slot.id == booking.slot_id).first()

    if not client or not slot:
        raise Exception("Invalid client or slot")

    for b in client.bookings:
        # Prevent booking multiple slots in same subject
        if b.slot.subject_id == slot.subject_id:
            raise Exception("Already booked a slot in this subject")

        # Prevent overlapping time slots
        if not (b.slot.end_time <= slot.start_time or b.slot.start_time >= slot.end_time):
            raise Exception("Slot overlaps with another booking")

    # Max 5 clients per slot
    if len(slot.bookings) >= 5:
        raise Exception("Slot full")

    # Create and store booking
    db_booking = Booking(client_id=booking.client_id, slot_id=booking.slot_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_all_slots(db: Session):
    # Get all slots and convert their time to subject's timezone
    slots = db.query(Slot).all()
    results = []

    for slot in slots:
        subject = db.query(Subject).filter(Subject.id == slot.subject_id).first()
        tz = pytz.timezone(subject.timezone)
        results.append({
            "id": slot.id,
            "subject_id": slot.subject_id,
            "start_time": slot.start_time.astimezone(tz).isoformat(),
            "end_time": slot.end_time.astimezone(tz).isoformat()
        })
    return results


def get_all_subjects_with_slots(db: Session):
    subjects = db.query(Subject).all()
    #now_utc = datetime.utcnow()
    result = []

    for subject in subjects:
        tz = pytz.timezone(subject.timezone)
        upcoming_slots = []
        now_local = datetime.now(tz).replace(tzinfo=None)
        for slot in subject.slots:
            # Only include future slots
            if slot.start_time > now_local:
                available_positions = 5 - len(slot.bookings)
                upcoming_slots.append(SlotInfo(
                    id=slot.id,
                    start_time=slot.start_time.astimezone(tz),
                    end_time=slot.end_time.astimezone(tz),
                    available_positions=available_positions
                ))

        # Sort slots by start time
        upcoming_slots.sort(key=lambda s: s.start_time)

        result.append({
            "id": subject.id,
            "name": subject.name,
            "instructor": subject.instructor,
            "timezone": subject.timezone,
            "slots": upcoming_slots
        })

    # Sort subjects by their earliest upcoming slot (if any)
    result.sort(key=lambda s: s["slots"][0].start_time if s["slots"] else datetime.max)

    return result