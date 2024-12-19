# Import necessary modules
import pytest
from fastapi.testclient import TestClient

from config import settings
from main import app


@pytest.fixture(scope="class", autouse=True)
def client():
    print("---setup---")
    with TestClient(app) as c:
        yield c
    print("---teardown---")


class Test_root:

    def test_hello(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"app_name": settings.app_name, "version": settings.version}
