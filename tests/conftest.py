#tests/conftest.py

from itertools import product
from itertools import product
import re
import pytest
import os
import json
import responses as responses_lib
from config.config import DEFAULT_USER, DEFAULT_PASSWORD, BASE_URL
from api_client.auth_api import login_user

def is_ci():
    return os.getenv("CI", "false").lower() == "true"

MOCK_PRODUCT = {
    "id": 1,
    "title": "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops",
    "price": 109.95,
    "description": "Your perfect pack for everyday use",
    "category": "men's clothing",
    "image": "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg",
    "rating": {"rate": 3.9, "count": 120}
}

@pytest.fixture(scope="session")
def auth_headers():
    if is_ci():
        return {"Authorization": "Bearer mock-ci-token"}
    response = login_user(DEFAULT_USER, DEFAULT_PASSWORD)
    if response.status_code == 201:
        token = response.json()["token"]
        return {"Authorization": f"Bearer {token}"}
    pytest.fail(f"Auth failed: {response.status_code} — {response.text}")

@pytest.fixture(autouse=True)
def mock_fakestore_in_ci(request):
    """
    Intercepts all HTTP calls to FakeStoreAPI when running in CI.
    FakeStoreAPI blocks GitHub Actions IP ranges — this fixture
    provides controlled responses so tests run without external dependencies.
    Not applied to UI tests which use Playwright, not requests.
    """
    if not is_ci():
        yield
        return

    if request.node.get_closest_marker('ui'):# Don't apply API mocks to UI tests which use Playwright, not requests.
        yield
        return

    def auth_callback(request): # This callback validates the request body for authentication, ensuring that both username and password are provided. It returns appropriate error responses for missing fields, simulates a successful authentication with a token for valid credentials, and returns an unauthorized response for invalid credentials.
        body = json.loads(request.body)
        username = body.get("username", "")
        password = body.get("password", "")
        if username == "" or password == "":
            return (400, {}, json.dumps({"error": "invalid request"}))
        if username == DEFAULT_USER and password == DEFAULT_PASSWORD:
            return (201, {}, json.dumps({"token": "mock-ci-token"}))
        return (401, {}, "")

    product_store = {}

    def create_callback(request): # This callback validates the request body for creating a product, ensuring required fields are present and correctly formatted. It returns appropriate error responses for invalid input, and simulates a successful creation with a new product ID when the input is valid.
        payload = json.loads(request.body)
    
        # Validate required fields
        if "title" not in payload:
            return (400, {}, json.dumps({"error": "title is required"}))
        if not isinstance(payload.get("title"), str) or payload["title"].strip() == "":
            return (400, {}, json.dumps({"error": "title must be a non-empty string"}))
        if "price" in payload and not isinstance(payload["price"], (int, float)):
            return (400, {}, json.dumps({"error": "price must be a number"}))
    
        product = {**payload, "id": 21}
        product_store[21] = product
        return (201, {}, json.dumps(product))
    
    def update_callback(request):
        payload = json.loads(request.body)
        product_id = int(request.url.split("/")[-1])
        product = {**payload, "id": product_id}
        product_store[product_id] = product
        return (200, {}, json.dumps(product))
    
    def get_product_by_id_callback(request):
        product_id = int(request.url.split("/")[-1])
        if product_id in product_store:
            return (200, {}, json.dumps(product_store[product_id]))
        return (200, {}, json.dumps({**MOCK_PRODUCT, "id": product_id}))

    def delete_callback(request):# This callback simulates the deletion of a product by returning the deleted product data based on the product ID in the URL. It allows tests to verify that the application correctly handles product deletion and processes the response from the API.
        product_id = int(request.url.split("/")[-1])
        return (200, {}, json.dumps({**MOCK_PRODUCT, "id": product_id}))

    with responses_lib.RequestsMock(assert_all_requests_are_fired=False) as rsps:

        rsps.add_callback(responses_lib.POST, f"{BASE_URL}/auth/login",
                         callback=auth_callback,
                         content_type="application/json")

        rsps.add(responses_lib.GET, f"{BASE_URL}/products",# This mock simulates the API's behavior when retrieving a list of products. By returning a predefined JSON array containing a single product with a 200 status code, it allows tests to verify that the application correctly retrieves and processes product data from the API.
                 json=[MOCK_PRODUCT], status=200)

        rsps.add(responses_lib.GET, f"{BASE_URL}/products/1",# This mock simulates the API's behavior when a valid product ID is requested. By returning a predefined JSON object representing the product with a 200 status code, it allows tests to verify that the application correctly retrieves and processes product data from the API.
                 json=MOCK_PRODUCT, status=200)

        rsps.add(responses_lib.GET, f"{BASE_URL}/products/9999",# This mock simulates the API's behavior when a non-existent product ID is requested. By returning an empty JSON object with a 200 status code, it allows tests to verify that the application correctly handles cases where a product is not found, without causing unexpected errors or crashes.
                 json={}, status=200)

        rsps.add(responses_lib.GET, f"{BASE_URL}/products/ABCD",# This mock simulates the API's behavior when an invalid product ID is requested. By returning an empty JSON object with a 200 status code, it allows tests to verify that the application correctly handles cases where a product is not found or the ID format is incorrect, without causing unexpected errors or crashes.
                 body=b"", status=200)

        rsps.add_callback(responses_lib.GET,
                re.compile(rf"{BASE_URL}/products/\d+"),
                callback=get_product_by_id_callback,
                content_type="application/json")

        rsps.add_callback(responses_lib.POST, f"{BASE_URL}/products",
                callback=create_callback,
                content_type="application/json")

        rsps.add_callback(responses_lib.PUT,
                 re.compile(rf"{BASE_URL}/products/\d+"),
                 callback=update_callback,
                 content_type="application/json")

        rsps.add_callback(responses_lib.DELETE,
                 re.compile(rf"{BASE_URL}/products/\d+"),
                 callback=delete_callback,
                 content_type="application/json")

        yield