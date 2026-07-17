from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_contact_validation_error() -> None:
    response = client.post(
        "/api/contact",
        json={
            "name": "И",
            "phone": "123",
            "email": "не email",
            "comment": "коротко",
        },
    )

    assert response.status_code == 422