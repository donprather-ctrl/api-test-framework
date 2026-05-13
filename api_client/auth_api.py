# api_client/auth_api.py

import requests
from config.config import BASE_URL

def login_user(username, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "username": username,
            "password": password
        }
    )
    return response


def get_current_user(headers=None):
    return requests.get(f"{BASE_URL}/auth/me", headers=headers)