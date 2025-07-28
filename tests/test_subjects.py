# tests/test_subjects.py
from tests.test_utils import create_subject

def test_create_subject(client):
    subject = create_subject(client, name="Dance", instructor="Ino")
    assert subject["name"] == "Dance"
    assert subject["instructor"] == "Ino"

def test_get_subjects(client):
    create_subject(client, name="Zumba", instructor="Lee")
    response = client.get("/subjects")
    assert response.status_code == 200
    subjects = response.json()
    assert any(s["name"] == "Zumba" for s in subjects)
