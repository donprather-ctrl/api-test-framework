#tests/test_auth_api.py

import requests
import pytest
from config.config import DEFAULT_USER , DEFAULT_PASSWORD
from api_client.auth_api import login_user
from utils.response_helpers import safe_json



@pytest.mark.smoke
@pytest.mark.api
def test_auth_api():
    response = login_user(DEFAULT_USER, DEFAULT_PASSWORD)
    
    if response.status_code == 403:
        pytest.skip("FakeStoreAPI returned 403 — likely IP blocking in CI")
    
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
    response = login_user("invalid_user", "wrong_password")
    
    if response.status_code == 403:
        pytest.skip("FakeStoreAPI returned 403 — likely IP blocking in CI")
    
    assert response.status_code == 401
    data = safe_json(response)
    assert data is None

