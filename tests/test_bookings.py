# tests/test_bookings.py
from tests.test_utils import create_subject, create_slot, create_client, create_booking

def test_create_booking(client):
    subject = create_subject(client)
    slot = create_slot(client, subject_id=subject["id"])
    test_client = create_client(client)

    booking_response = create_booking(client, test_client["id"], slot["id"])

    assert booking_response.status_code == 200
    booking = booking_response.json()
    assert booking["client_id"] == test_client["id"]
    assert booking["slot_id"] == slot["id"]


def test_double_booking_not_allowed(client):
    subject = create_subject(client, name="Pilates")
    slot = create_slot(client, subject_id=subject["id"])
    test_client = create_client(client, name="Naruto")

    # First booking
    create_booking(client, test_client["id"], slot["id"])

    # Second (duplicate) booking attempt
    duplicate = create_booking(client, test_client["id"], slot["id"])

    assert duplicate.status_code == 400
