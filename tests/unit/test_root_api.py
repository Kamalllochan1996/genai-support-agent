from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "GenAI Support Agent API is running"
    )

    assert "X-Request-ID" in response.headers