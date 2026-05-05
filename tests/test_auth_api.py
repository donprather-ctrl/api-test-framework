#tests/test_auth_api.py

import pytest
import os
from config.config import DEFAULT_USER, DEFAULT_PASSWORD
from api_client.auth_api import login_user
from utils.response_helpers import safe_json

def is_ci():
    return os.getenv("CI", "false").lower() == "true"

@pytest.mark.smoke
@pytest.mark.api
def test_auth_api():
    if is_ci():
        pytest.skip("Auth test skipped in CI — FakeStoreAPI blocks GitHub Actions IPs. Validated locally.")
    
    response = login_user(DEFAULT_USER, DEFAULT_PASSWORD)
    assert response.status_code == 201
    data = safe_json(response)
    assert data is not None
    assert "token" in data
    token = data["token"]
    assert isinstance(token, str)
    assert len(token) > 10

@pytest.mark.smoke
@pytest.mark.api
def test_auth_api_negative():
    if is_ci():
        pytest.skip("Auth test skipped in CI — FakeStoreAPI blocks GitHub Actions IPs. Validated locally.")
    
    response = login_user("invalid_user", "wrong_password")
    assert response.status_code == 401
    data = safe_json(response)
    assert data is None