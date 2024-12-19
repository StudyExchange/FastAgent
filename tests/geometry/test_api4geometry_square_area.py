import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="class")
def client():
    with TestClient(app) as c:
        yield c


class Test_geometry_square_area:
    def test_square_area_valid(self, client):
        # Test valid input for square area calculation
        response = client.post("/geometry/square_area/", params={"side": 5})
        assert response.status_code == 200
        assert response.json() == 25

    def test_square_area_zero(self, client):
        # Test side length of zero
        response = client.post("/geometry/square_area/", params={"side": 0})
        assert response.status_code == 400
        assert response.json()["detail"] == "Side must be a positive number"

    def test_square_area_negative(self, client):
        # Test negative side length
        response = client.post("/geometry/square_area/", params={"side": -3})
        assert response.status_code == 400
        assert response.json()["detail"] == "Side must be a positive number"

    def test_square_area_non_number(self, client):
        # Test non-numeric side input
        response = client.post("/geometry/square_area/", params={"side": "five"})
        assert response.status_code == 422
        assert "Input should be a valid number, unable to parse string as a number" in response.json()["detail"][0]["msg"]
