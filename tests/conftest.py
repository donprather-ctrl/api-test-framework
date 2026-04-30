#tests/conftest.py

import pytest
from config.config import DEFAULT_USER , DEFAULT_PASSWORD
from api_client.auth_api import login_user

@pytest.fixture(scope="session")

def auth_headers():

    response = login_user(DEFAULT_USER, DEFAULT_PASSWORD)

    if response.status_code == 201:
        data = response.json()
        token = data["token"]

        headers = {
            "Authorization": f"Bearer {token}"
        }
        return headers

    else:
        raise Exception("Failed to obtain auth token")

