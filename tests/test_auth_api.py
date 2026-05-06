#tests/test_auth_api.py

import pytest
import os
from config.config import DEFAULT_USER, DEFAULT_PASSWORD
from api_client.auth_api import login_user
from utils.response_helpers import safe_json


@pytest.mark.smoke
@pytest.mark.api
def test_auth_valid_credentials():
    """Valid credentials return 201 and a token."""
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
@pytest.mark.parametrize("username,password,description,expected_status", [
    ("invalid_user",  DEFAULT_PASSWORD, "wrong username, correct password",  401),
    (DEFAULT_USER,    "wrong_password", "correct username, wrong password",   401),
    ("invalid_user",  "wrong_password", "both wrong",                         401),
    ("",              DEFAULT_PASSWORD, "empty username",                      400),
    (DEFAULT_USER,    "",               "empty password",                      400),
    ("",              "",               "both empty",                          400),
])

def test_auth_invalid_credentials(username, password, description, expected_status):
    """Invalid credentials never return a token. Empty fields return 400, wrong credentials return 401."""
    response = login_user(username, password)
    assert response.status_code == expected_status, f"Failed scenario: {description}"
    data = safe_json(response)
    if data is not None:
        assert "token" not in data, f"Security: token must not be returned on failed auth — {description}"