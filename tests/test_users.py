from fastapi.testclient import TestClient
from app.main import app
from app.database.mysql import get_connection

client = TestClient(app)

def setup_function():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    cursor.close()
    conn.close()


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user():
    user = {"id": 1, "name": "Ana", "email": "ana@email.com"}
    response = client.post("/users", json=user)
    assert response.status_code == 200
    assert response.json()["name"] == "Ana"


def test_get_user_by_id():
    client.post("/users", json={"id": 1, "name": "Ana", "email": "ana@email.com"})
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_delete_user():
    client.post("/users", json={"id": 1, "name": "Ana", "email": "ana@email.com"})
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted"
