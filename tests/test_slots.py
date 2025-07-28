# tests/test_slots.py
from tests.test_utils import create_subject, create_slot

def test_create_slot(client):
    subject = create_subject(client, name="Cardio", instructor="Neji")
    slot = create_slot(client, subject_id=subject["id"])
    assert slot["subject_id"] == subject["id"]

def test_get_slots_by_subject(client):
    subject = create_subject(client, name="Strength", instructor="Shino")
    create_slot(client, subject_id=subject["id"], start="2025-07-30T12:00:00", end="2025-07-30T13:00:00")

    response = client.get("/subjects")
    assert response.status_code == 200
    subjects = response.json()

    found = next(s for s in subjects if s["id"] == subject["id"])
    assert len(found["slots"]) >= 1
