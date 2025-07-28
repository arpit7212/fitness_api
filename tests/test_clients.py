from tests.test_utils import create_client

def test_create_client(client):
    created = create_client(client, name="Itachi")
    assert created["name"] == "Itachi"

def test_get_clients(client):
    create_client(client, name="Kakashi")
    response = client.get("/clients")
    assert response.status_code == 200
    clients = response.json()
    assert any(c["name"] == "Kakashi" for c in clients)