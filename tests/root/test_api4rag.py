import pytest
from fastapi.testclient import TestClient

from config import settings
from main import app


@pytest.fixture(scope="class", autouse=True)
def client():
    with TestClient(app) as c:
        yield c


class Test_rag:

    def test_rag_with_valid_input(self, client):
        """
        Test /rag/ endpoint with valid input
        """
        messages = [{"role": "user", "content": "Hello, who are you?"}]
        response = client.post("/rag/", json=messages)
        assert response.status_code == 200

    def test_rag_with_invalid_input(self, client):
        """
        Test /rag/ endpoint with invalid input (non-list type)
        """
        messages = "invalid input"
        response = client.post("/rag/", json=messages)
        assert response.status_code == 422
        assert "valid list" in response.text.lower()

    def test_rag_with_empty_input(self, client):
        """
        Test /rag/ endpoint with empty input list
        """
        messages = []
        response = client.post("/rag/", json=messages)
        assert response.status_code == 422
        assert "messages is empty" in response.text.lower()

    def test_rag_with_llm_self_ability(self, client):
        """
        Test /rag/ endpoint with llm self ability
        """
        messages = [{"role": "user", "content": "Which city is called mountain city in China?"}]
        response = client.post("/rag/", json=messages)
        assert response.status_code == 200
        assert "chongqing" in response.text.lower()

    def test_rag_with_unavailable_tool(self, client):
        """
        Test /rag/ endpoint with unavailable tool
        """
        messages = [{"role": "user", "content": "What's the weather like in Chongqing today?"}]
        response = client.post("/rag/", json=messages)
        assert response.status_code == 200
        assert "chongqing" in response.text.lower()

    def test_rag_with_vector_similarity(self, client):
        """
        Test /rag/ endpoint with vector similarity
        """
        messages = [{"role": "user", "content": "How setup a file server based on python?"}]
        response = client.post("/rag/", json=messages)
        assert response.status_code == 200
        assert "python3 -m http.server".lower() in response.text.lower()
