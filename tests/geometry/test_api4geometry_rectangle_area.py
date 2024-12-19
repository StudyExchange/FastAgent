import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="class")
def client():
    with TestClient(app) as c:
        yield c


class Test_geometry_rectangle_area:
    def test_rectangle_area_valid(self, client):
        # Test valid input for rectangle area calculation
        response = client.post("/geometry/rectangle_area/", params={"length": 5, "width": 4})
        assert response.status_code == 200
        assert response.json() == 20

    def test_rectangle_area_length_zero(self, client):
        # Test length of zero
        response = client.post("/geometry/rectangle_area/", params={"length": 0, "width": 4})
        assert response.status_code == 400
        assert response.json()["detail"] == "Length and width must be positive numbers"

    def test_rectangle_area_width_negative(self, client):
        # Test negative width
        response = client.post("/geometry/rectangle_area/", params={"length": 5, "width": -4})
        assert response.status_code == 400
        assert response.json()["detail"] == "Length and width must be positive numbers"

    def test_rectangle_area_both_negative(self, client):
        # Test negative length and width
        response = client.post("/geometry/rectangle_area/", params={"length": -5, "width": -4})
        assert response.status_code == 400
        assert response.json()["detail"] == "Length and width must be positive numbers"

    def test_rectangle_area_non_number(self, client):
        # Test non-numeric length input
        response = client.post("/geometry/rectangle_area/", params={"length": "five", "width": 4})
        assert response.status_code == 422
        assert "Input should be a valid number, unable to parse string as a number" in response.json()["detail"][0]["msg"]
