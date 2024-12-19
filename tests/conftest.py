import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import config

@pytest.fixture
def client():
    """
    Provide a FastAPI test client for testing API endpoints.

    Returns:
        TestClient: A FastAPI test client instance.
    """
    return TestClient(app)