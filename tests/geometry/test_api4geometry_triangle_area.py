import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="class")
def client():
    with TestClient(app) as c:
        yield c


class Test_geometry_triangle_area:
    def test_triangle_area_valid(self, client):
        # Test valid input for triangle area calculation
        response = client.post("/geometry/triangle_area/", params={"base": 4, "height": 3})
        assert response.status_code == 200
        assert response.json() == 6.0

    def test_triangle_area_base_zero(self, client):
        # Test base length of zero
        response = client.post("/geometry/triangle_area/", params={"base": 0, "height": 3})
        assert response.status_code == 400
        assert response.json()["detail"] == "Base and height must be positive numbers"

    def test_triangle_area_height_negative(self, client):
        # Test negative height
        response = client.post("/geometry/triangle_area/", params={"base": 4, "height": -3})
        assert response.status_code == 400
        assert response.json()["detail"] == "Base and height must be positive numbers"

    def test_triangle_area_both_negative(self, client):
        # Test negative base and height
        response = client.post("/geometry/triangle_area/", params={"base": -4, "height": -3})
        assert response.status_code == 400
        assert response.json()["detail"] == "Base and height must be positive numbers"

    def test_triangle_area_non_number(self, client):
        # Test non-numeric base input
        response = client.post("/geometry/triangle_area/", params={"base": "four", "height": 3})
        assert response.status_code == 422
        assert "Input should be a valid number, unable to parse string as a number" in response.json()["detail"][0]["msg"]
