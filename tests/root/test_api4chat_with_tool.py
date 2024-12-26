import pytest
from fastapi.testclient import TestClient

from config import settings
from main import app


@pytest.fixture(scope="class", autouse=True)
def client():
    with TestClient(app) as c:
        yield c


class Test_chat_with_tool:

    def test_chat_with_valid_input(self, client):
        """
        Test /chat/ endpoint with valid input
        """
        messages = [{"role": "user", "content": "Hello, who are you?"}]
        response = client.post("/chat/", json=messages)
        assert response.status_code == 200

    def test_chat_with_invalid_input(self, client):
        """
        Test /chat/ endpoint with invalid input (non-list type)
        """
        messages = "invalid input"
        response = client.post("/chat/", json=messages)
        assert response.status_code == 422
        assert "valid list" in response.text.lower()

    def test_chat_with_empty_input(self, client):
        """
        Test /chat/ endpoint with empty input list
        """
        messages = []
        response = client.post("/chat/", json=messages)
        assert response.status_code == 422
        assert "messages is empty" in response.text.lower()

    def test_chat_with_llm_self_ability(self, client):
        """
        Test /chat/ endpoint with llm self ability
        """
        messages = [{"role": "user", "content": "Which city is called mountain city in China?"}]
        response = client.post("/chat/", json=messages)
        assert response.status_code == 200
        assert "chongqing" in response.text.lower()

    def test_chat_with_unavailable_tool(self, client):
        """
        Test /chat/ endpoint with unavailable tool
        """
        messages = [{"role": "user", "content": "What's the weather like in Chongqing today?"}]
        response = client.post("/chat/", json=messages)
        assert response.status_code == 200
        assert "chongqing" in response.text.lower()

    def test_chat_with_tool(self, client):
        """
        Test /chat/ endpoint with tool
        """
        messages = [{"role": "user", "content": "Can you help me calculate the area of a aquare with a side of 5cm?"}]
        response = client.post("/chat/", json=messages)
        assert response.status_code == 200
        assert "25" in response.text.lower()

    def test_chat_with_tool_missing_parameters(self, client):
        """
        Test /chat/ endpoint with tool missing parameters
        """
        messages = [{"role": "user", "content": "Can you help me calculate the area of a rectangle with a height of 5cm?"}]
        response = client.post("/chat/", json=messages)
        assert response.status_code == 200
        assert "need" in response.text.lower()

    def test_chat_with_tool_supplementary_parameters(self, client):
        """
        Test /chat/ endpoint with tool supplementary parameters
        """
        messages = [
            {
                "role": "user",
                "content": "Can you help me calculate the area of a rectangle with a height of 5cm?",
            },
            {
                "role": "assistant",
                "content": "Of course, to calculate the area of a rectangle, we need both the height and the width (or length). "
                + "You've mentioned the height is 5 cm. Could you please also provide the width (or length) of the rectangle? "
                + "Once I have both measurements, I can help you find the area.",
            },
            {
                "role": "user",
                "content": "Length is 2cm",
            },
        ]
        response = client.post("/chat/", json=messages)
        assert response.status_code == 200
        assert "10" in response.text.lower()

    def test_chat_with_multi_tool(self, client):
        """
        Test /chat/ endpoint with multi tool
        """
        messages = [
            {
                "role": "user",
                "content": "First, help me calculate the area of a square with a side length of 5cm, and then calculate the area of a triangle with a base of 4cm and a height of 6cm.",
            }
        ]
        response = client.post("/chat/", json=messages)
        assert response.status_code == 200
        assert "25" in response.text.lower()

    def test_chat_with_multi_tool_missing_parameters(self, client):
        """
        Test /chat/ endpoint with multi tool missing parameters
        """
        messages = [
            {
                "role": "user",
                "content": "First, help me calculate the area of a square with a side length of 5cm, and then calculate the area of a triangle with a height of 6cm.",
            }
        ]
        response = client.post("/chat/", json=messages)
        assert response.status_code == 200
        assert "5" in response.text.lower()

    def test_chat_with_multi_tool_supplementary_parameters(self, client):
        """
        Test /chat/ endpoint with multi tool supplementary parameters
        """
        messages = [
            {
                "role": "user",
                "content": "First, help me calculate the area of a square with a side length of 5cm, and then calculate the area of a triangle with a height of 6cm.",
            },
            {
                "role": "assistant",
                "content": "The area of the square with a side length of 5 cm is 25.0 square centimeters. "
                + "To calculate the area of a triangle, we use the formula: \(\text{Area} = \frac{1}{2} \times \text{base} \times \text{height}\). "
                + "However, you've only provided the height of the triangle (6 cm), and the base length is missing. "
                + "Could you please provide the length of the base? With that information, I can help you calculate the area of the triangle.",
            },
            {
                "role": "user",
                "content": "base=4cm",
            },
        ]
        response = client.post("/chat/", json=messages)
        assert response.status_code == 200
        assert "12" in response.text.lower()
