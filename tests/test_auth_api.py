#tests/test_auth_api.py

import requests
from config.config import DEFAULT_USER , DEFAULT_PASSWORD
from api_client.auth_api import login_user





def test_auth_api():

    response = login_user(DEFAULT_USER, DEFAULT_PASSWORD)

    assert response.status_code == 201  # observed behavior

    data = response.json()

    assert isinstance(data, dict)
    assert "token" in data

    token = data["token"]

    assert isinstance(token, str)
    assert len(token) > 10
    print(f"\n INFO: token is {token}")

def test_auth_api_negative():

    response = login_user("invalid_user", "wrong_password")

    assert response.status_code == 401

