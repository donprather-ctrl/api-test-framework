# tests/test_users_api.py

import pytest
import os
CI = os.getenv("CI", "false").lower() == "true"
from api_client.users_api import get_all_users, get_user_by_id, create_user, update_user, delete_user
from utils.validators import validate_user, validate_user_write_response
from utils.response_helpers import safe_json
from utils.data_loader import load


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
    payload = load("users.json")["create_valid_user"]
    response = create_user(payload, headers=auth_headers)
    assert response.status_code == 201
    data = safe_json(response)
    assert data is not None
    assert isinstance(data, dict)
    validate_user_write_response(data, payload)


@pytest.mark.api
@pytest.mark.smoke
def test_update_user(auth_headers):
    payload = load("users.json")["update_user"]
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
    """Validates full user lifecycle: CREATE → GET → UPDATE → DELETE."""

    payload = load("users.json")["create_e2e_user"]
    response = create_user(payload, headers=auth_headers)
    assert response.status_code == 201
    data = safe_json(response)
    assert data is not None
    validate_user_write_response(data, payload)

    response = get_user_by_id(1, headers=auth_headers)
    assert response.status_code == 200
    data = safe_json(response)
    assert data is not None
    validate_user(data)

    updated_payload = load("users.json")["update_e2e_user"]
    response = update_user(1, updated_payload, headers=auth_headers)
    assert response.status_code == 200
    data = safe_json(response)
    validate_user_write_response(data, updated_payload)

    response = delete_user(1, headers=auth_headers)
    assert response.status_code == 200
    data = safe_json(response)
    assert data.get("isDeleted") is True


@pytest.mark.api
@pytest.mark.regression
def test_create_user_api_behavior_observations():
    """
    Documents known dummyjson behavior on POST /users/add.
    These are observations, not defects — dummyjson is a testing tool
    with no real validation or auth enforcement on write operations.

    Known behaviors:
    - Auth header not required — unauthenticated creates return 201
    - Missing fields default to empty string or null — not rejected
    - Integer values accepted for string fields — no type enforcement
    - Duplicate emails accepted — no uniqueness validation
    """
    # No auth header — should require auth but doesn't
    response = create_user({"firstName": "Test", "lastName": "Test", "email": "test@test.com"})
    assert response.status_code == 201, "Observed: unauthenticated create returns 201"

    # Missing firstName — defaults to empty string
    response = create_user({"lastName": "Test", "email": "test@test.com"})
    assert response.status_code == 201
    data = safe_json(response)
    assert data["firstName"] == "", "Observed: missing firstName defaults to empty string"

    # Integer firstName — accepted without type coercion
    response = create_user({"firstName": 123, "lastName": "Test", "email": "test@test.com"})
    assert response.status_code == 201
    data = safe_json(response)
    assert data["firstName"] == 123, "Observed: integer firstName echoed back unchanged"