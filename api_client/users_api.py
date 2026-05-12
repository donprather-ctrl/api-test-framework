# api_client/users_api.py

import requests
from config.config import BASE_URL

def get_all_users(headers=None):
    return requests.get(f"{BASE_URL}/users", headers=headers)

def get_user_by_id(user_id, headers=None):
    return requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)

def create_user(payload, headers=None):
    return requests.post(f"{BASE_URL}/users/add", json=payload, headers=headers)

def update_user(user_id, payload, headers=None):
    return requests.put(f"{BASE_URL}/users/{user_id}", json=payload, headers=headers)

def delete_user(user_id, headers=None):
    return requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)