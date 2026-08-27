from fastapi.testclient import TestClient

from app.api.dependencies import get_chat_service
from app.api.main import app
from app.api.services.chat_service import ChatService
from app.api.services.fake_llm import FakeLLM


def get_test_chat_service() -> ChatService:

    return ChatService(
        llm_service=FakeLLM(),
    )


app.dependency_overrides[
    get_chat_service
] = get_test_chat_service


client = TestClient(app)


def test_chat_endpoint():

    response = client.post(
        "/api/v1/chat",
        json={
            "question": "How many casual leaves can an employee take?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == (
        "How many casual leaves can an employee take?"
    )

    assert data["answer"] == (
        "This is a fake LLM response."
    )

    assert "X-Request-ID" in response.headers


def test_chat_endpoint_missing_question():

    response = client.post(
        "/api/v1/chat",
        json={},
    )

    assert response.status_code == 422


def test_chat_endpoint_invalid_question_type():

    response = client.post(
        "/api/v1/chat",
        json={
            "question": 12345,
        },
    )

    assert response.status_code == 422