# seed_data.py

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from app import crud, schemas
from datetime import datetime, timedelta
from datetime import timezone
from app import models

# Create DB tables
Base.metadata.create_all(bind=engine)

# Open DB session
db: Session = SessionLocal()

# Seed Subjects
subject_data = [
    {"name": "ninjutsu", "timezone": "Asia/Kolkata", "instructor": "kakashi"},
    {"name": "taijutsu", "timezone": "UTC", "instructor": "might guy"},
    {"name": "genjutsu", "timezone": "America/New_York", "instructor": "itachi"},
]

subjects = []
for data in subject_data:
    subj_schema = schemas.SubjectCreate(**data)
    subject = crud.create_subject(db, subj_schema)
    subjects.append(subject)

# Seed Clients
client_names = ["sasuke", "sakura", "naruto"]
clients = []
for name in client_names:
    client = crud.create_client(db, schemas.ClientCreate(name=name))
    clients.append(client)

# Seed Slots for each subject (2 future slots)
for subject in subjects:
    #now = datetime.utcnow().replace(tzinfo=None)
    now = datetime.now(timezone.utc)
    for i in range(2):
        start_time = now + timedelta(days=i + 1, hours=9)
        end_time = start_time + timedelta(hours=1)
        slot = crud.create_slot(
            db,
            schemas.SlotCreate(
                subject_id=subject.id,
                start_time=start_time,
                end_time=end_time
            )
        )

# Optional: Seed a few bookings
all_slots = db.query(models.Slot).all()
for i, slot in enumerate(all_slots[:3]):
    crud.create_booking(
        db,
        schemas.BookingCreate(client_id=clients[i % len(clients)].id, slot_id=slot.id)
    )

db.close()
print("✅ Seed data inserted successfully.")
