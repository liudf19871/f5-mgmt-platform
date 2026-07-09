import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login():
    response = client.post("/api/auth/login", json={"username": "test", "password": "test"})
    assert response.status_code == 401