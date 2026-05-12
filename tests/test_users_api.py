# tests/test_users_api.py

import pytest
from api_client.users_api import get_all_users, get_user_by_id, create_user, update_user, delete_user
from utils.validators import validate_user, validate_user_write_response
from utils.response_helpers import safe_json


@pytest.mark.api
@pytest.mark.smoke
def test_get_all_users(auth_headers):
    response = get_all_users(headers=auth_headers)
    assert response.status_code == 200
    data = safe_json(response)
    assert data is not None, "Get all users: expected JSON response"
    assert "users" in data, "Get all users: expected 'users' key in response"
    assert isinstance(data["users"], list), "Get all users: expected a list"
    assert len(data["users"]) > 0, "Get all users: list is empty"
    validate_user(data["users"][0])


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.parametrize("user_id, expected_status", [
    (1,      200),
    (9999,   404),
    ("ABCD", 400),
])
def test_get_user_by_id(user_id, expected_status, auth_headers):
    response = get_user_by_id(user_id, headers=auth_headers)
    assert response.status_code == expected_status
    if expected_status == 200:
        data = safe_json(response)
        assert data is not None
        validate_user(data)
        assert data["id"] == user_id


@pytest.mark.api
@pytest.mark.smoke
def test_create_user(auth_headers):
    payload = {
        "firstName": "Test",
        "lastName": "User",
        "email": "testuser@test.com",
        "age": 30
    }
    response = create_user(payload, headers=auth_headers)
    assert response.status_code == 201
    data = safe_json(response)
    assert data is not None
    assert isinstance(data, dict)
    validate_user_write_response(data, payload)


@pytest.mark.api
@pytest.mark.smoke
def test_update_user(auth_headers):
    payload = {
        "firstName": "Updated",
        "lastName": "User",
        "email": "updated@test.com"
    }
    response = update_user(1, payload, headers=auth_headers)
    assert response.status_code == 200
    data = safe_json(response)
    assert data is not None
    assert isinstance(data, dict)
    validate_user_write_response(data, payload)


@pytest.mark.api
@pytest.mark.smoke
def test_delete_user(auth_headers):
    response = delete_user(1, headers=auth_headers)
    assert response.status_code == 200
    data = safe_json(response)
    assert data is not None
    assert data.get("isDeleted") is True


@pytest.mark.api
@pytest.mark.regression
def test_user_e2e_workflow(auth_headers):
    """Validates full user lifecycle: CREATE → GET (seed) → UPDATE → DELETE."""

    # Create
    payload = {
        "firstName": "E2E",
        "lastName": "TestUser",
        "email": "e2e@test.com",
        "age": 25
    }
    response = create_user(payload, headers=auth_headers)
    assert response.status_code == 201
    data = safe_json(response)
    assert data is not None
    validate_user_write_response(data, payload)

    # Get — use known seed user since dummyjson doesn't persist created users
    response = get_user_by_id(1, headers=auth_headers)
    assert response.status_code == 200
    data = safe_json(response)
    assert data is not None
    validate_user(data)

    # Update
    updated_payload = {
        "firstName": "E2E Updated",
        "lastName": "TestUser",
        "email": "e2e_updated@test.com"
    }
    response = update_user(1, updated_payload, headers=auth_headers)
    assert response.status_code == 200
    data = safe_json(response)
    validate_user_write_response(data, updated_payload)

    # Delete
    response = delete_user(1, headers=auth_headers)
    assert response.status_code == 200
    data = safe_json(response)
    assert data.get("isDeleted") is True