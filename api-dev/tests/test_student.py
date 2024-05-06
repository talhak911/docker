from fastapi.testclient import TestClient
from api.main import app

def test_students():
    client =TestClient(app=app)
    response =client.get("/root")
    assert response.status_code == 200
    assert response.json() =="root"