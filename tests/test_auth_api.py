# tests/test_auth_api.py

import pytest
from config.config import DEFAULT_USER, DEFAULT_PASSWORD
from api_client.auth_api import login_user
from utils.response_helpers import safe_json


@pytest.mark.smoke
@pytest.mark.api
def test_auth_valid_credentials():
    """Valid credentials return 200 and an access token."""
    response = login_user(DEFAULT_USER, DEFAULT_PASSWORD)
    assert response.status_code == 200
    data = safe_json(response)
    assert data is not None
    assert "accessToken" in data
    assert isinstance(data["accessToken"], str)
    assert len(data["accessToken"]) > 10


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize("username, password, description", [
    ("invalid_user",  DEFAULT_PASSWORD, "wrong username, correct password"),
    (DEFAULT_USER,    "wrong_password", "correct username, wrong password"),
    ("invalid_user",  "wrong_password", "both wrong"),
    ("",              DEFAULT_PASSWORD, "empty username"),
    (DEFAULT_USER,    "",               "empty password"),
    ("",              "",               "both empty"),
])
def test_auth_invalid_credentials(username, password, description):
    """Invalid credentials always return 400 — no token issued."""
    response = login_user(username, password)
    assert response.status_code == 400, f"Failed scenario: {description}"
    data = safe_json(response)
    if data is not None:
        assert "accessToken" not in data, f"Security: token must not be returned on failed auth — {description}"