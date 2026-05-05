#tests/conftest.py
import pytest
import os
from config.config import DEFAULT_USER, DEFAULT_PASSWORD
from api_client.auth_api import login_user

def is_ci():
    return os.getenv("CI", "false").lower() == "true"

@pytest.fixture(scope="session")
def auth_headers():
    if is_ci():
        # FakeStoreAPI blocks GitHub Actions IP ranges.
        # Return a mock token in CI — auth behavior is validated locally.
        return {"Authorization": "Bearer mock-token-for-ci"}

    response = login_user(DEFAULT_USER, DEFAULT_PASSWORD)

    if response.status_code == 403:
        pytest.skip(f"Auth unavailable — API returned {response.status_code}. "
                    f"Likely IP blocking in CI environment.")

    if response.status_code == 201:
        token = response.json()["token"]
        return {"Authorization": f"Bearer {token}"}

    pytest.fail(f"Auth failed unexpectedly: {response.status_code} — {response.text}")