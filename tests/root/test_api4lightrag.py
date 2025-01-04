import pytest
from fastapi.testclient import TestClient

from config import settings
from main import app


@pytest.fixture(scope="class", autouse=True)
def client():
    with TestClient(app) as c:
        yield c


class Test_lightrag:

    def test_lightrag_with_valid_input(self, client):
        """
        Test /lightrag/ endpoint with valid input
        """
        messages = [{"role": "user", "content": "Hello, who are you?"}]
        response = client.post("/lightrag/", json=messages)
        assert response.status_code == 200

    def test_lightrag_with_invalid_input(self, client):
        """
        Test /lightrag/ endpoint with invalid input (non-list type)
        """
        messages = "invalid input"
        response = client.post("/lightrag/", json=messages)
        assert response.status_code == 422
        assert "valid list" in response.text.lower()

    def test_lightrag_with_empty_input(self, client):
        """
        Test /lightrag/ endpoint with empty input list
        """
        messages = []
        response = client.post("/lightrag/", json=messages)
        assert response.status_code == 422
        assert "messages is empty" in response.text.lower()

    def test_lightrag_with_tesla_born(self, client):
        """
        Test /lightrag/ endpoint with vector similarity
        """
        messages = [{"role": "user", "content": "What year was Tesla born?"}]
        response = client.post("/lightrag/", json=messages)
        assert response.status_code == 200
        assert "1856" in response.text.lower()
