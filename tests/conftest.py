import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app, activities


@pytest.fixture
def fresh_activities():
    """Provide a fresh copy of the activities database for each test"""
    return deepcopy(activities)


@pytest.fixture
def client(fresh_activities, monkeypatch):
    """Provide a FastAPI TestClient with isolated activities data"""
    # Replace the global activities dict with our fresh copy for this test
    monkeypatch.setattr("src.app.activities", fresh_activities)
    return TestClient(app)
