#shared test functions used by all
from app.database import Base, engine


def create_subject(client, name="Yoga", timezone="Asia/Kolkata", instructor="Naruto"):
    response = client.post("/subjects", json={
        "name": name,
        "timezone": timezone,
        "instructor": instructor
    })
    assert response.status_code == 200
    return response.json()


def create_slot(client, subject_id, start="2025-07-30T10:00:00", end="2025-07-30T11:00:00"):
    response = client.post("/slots", json={
        "subject_id": subject_id,
        "start_time": start,
        "end_time": end
    })
    assert response.status_code == 200
    return response.json()


def create_client(client, name="Sasuke"):
    response = client.post("/clients", json={"name": name})
    assert response.status_code == 200
    return response.json()


def create_booking(client, client_id, slot_id):
    response = client.post("/bookings", json={
        "client_id": client_id,
        "slot_id": slot_id
    })
    return response

def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)