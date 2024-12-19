import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="class")
def client():
    with TestClient(app) as c:
        yield c


class Test_geometry_hello:
    def test_hello(self, client):
        # Test the /geometry/hello/ endpoint
        response = client.get("/geometry/hello/")
        assert response.status_code == 200
        assert response.json() == "geometry works OK!"
