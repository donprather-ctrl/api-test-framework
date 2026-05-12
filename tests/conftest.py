# tests/conftest.py

import pytest
from config.config import DEFAULT_USER, DEFAULT_PASSWORD
from api_client.auth_api import login_user

@pytest.fixture(scope="session")
def auth_headers():
    response = login_user(DEFAULT_USER, DEFAULT_PASSWORD)
    if response.status_code == 200:
        token = response.json()["accessToken"]
        return {"Authorization": f"Bearer {token}"}
    pytest.fail(f"Auth failed: {response.status_code} — {response.text}")