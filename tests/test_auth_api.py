# tests/test_auth_api.py

import pytest
from config.config import DEFAULT_USER, DEFAULT_PASSWORD
from api_client.auth_api import login_user
import time
from utils.response_helpers import safe_json, decode_jwt_payload


@pytest.mark.smoke
@pytest.mark.api
def test_auth_valid_credentials():
    """Valid credentials return 200 and a well-formed JWT access token."""
    
    response = login_user(DEFAULT_USER, DEFAULT_PASSWORD)
    assert response.status_code == 200
    
    data = safe_json(response)
    assert data is not None
    assert "accessToken" in data
    token = data["accessToken"]
    

    # JWT structure validation
    assert isinstance(token, str), "Token is not a valid string" 
    assert len(token) > 10, "Token is too short" 
    parts = token.split(".")
    assert len(parts) == 3, "Token is not a valid JWT — expected 3 parts"
    assert all(len(part) > 0 for part in parts), "JWT contains empty segments"

    # JWT payload validation
    payload = decode_jwt_payload(token)
    assert payload is not None, "JWT payload could not be decoded"
    assert "id" in payload, "JWT missing 'id' claim"
    assert "username" in payload, "JWT missing 'username' claim"
    assert "exp" in payload, "JWT missing 'exp' claim"
    assert "iat" in payload, "JWT missing 'iat' claim"
    assert payload["exp"] > time.time(), "Token is already expired"
    assert payload["username"] == DEFAULT_USER, "JWT username doesn't match login credentials"


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