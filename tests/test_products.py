#tests/test_products_api.py

## Tests contained in this file:
### -test_get_all_products
### -test_get_product_by_id
### -test_create_product
### -test_update_product
### -test_delete_product
### -test_product_workflow (e2e test.. create product, get product details, update product, delete product)

import pytest
from api_client.products_api import get_all_products, get_product_by_id, create_product, update_product, delete_product
from utils.validators import validate_product, validate_write_response
from utils.response_helpers import safe_json

def test_get_all_products(auth_headers):

    response = get_all_products(headers=auth_headers) #call the api client for get all products
    assert response.status_code == 200
    data = safe_json(response) #safe_json is a helper function. Returns None if the response returns a non-JSON response.
    assert data is not None, "Get all Products: Expected JSON response but got None"
    assert isinstance(data, list), "Get all Products: Expected a list in the response"
    assert len(data) > 0, "Get all Products: JSON response is empty. Expected at least one product"
    validate_product(data[0]) #pulls the first item (a dictionary defining the first product) in the list. validate_product is a helper function in utils/validators.py#


#_________________________________________________________
# LEARNING NOTE: The decorator requires two primary arguments...
# FIRST ...a string containing the parameter names (comma-separated if more than one)
# SECOND ...an iterable (usually a list of tuples) containing the test values.
@pytest.mark.parametrize(
    "product_id, is_valid",
    [
        (1, True),        # valid (placeholder)
        ("ABCD", False),  # invalid type
        (9999, False)     # out of range
    ]
)


def test_get_product_by_id(product_id, is_valid, auth_headers):

    # Arrange
    if is_valid:
        list_response = get_all_products(headers=auth_headers)
        assert list_response.status_code == 200
        list_data = safe_json(list_response)
        assert list_data is not None, "Get All Products: Expected JSON response but got None"
        assert isinstance(list_data, list), "Get all Products: Expected a list in the response"
        assert len(list_data) > 0, "Get All Products: JSON response is empty. Expected at least one product"
        product_id = list_data[0]["id"]

    # Act
    response = get_product_by_id(product_id, headers=auth_headers) #call the api client for get product by id
    assert response.status_code in [200, 404]
    product_data = safe_json(response) #returns either the body (in json) or "None" if the body is not valid json.


    if is_valid: #product ID is valid
        assert response.status_code == 200
        assert product_data is not None, "Get Product by ID: expected a json response" #assert that product_data can be safely converted to json
        assert isinstance(product_data, dict), "Get Product By ID: Expected a dict in the response"
        validate_product(product_data)
        assert product_data["id"] == product_id

    else: #product ID is not valid
        if product_data is not None:
            assert isinstance(product_data, dict), "Get Product By ID: Expected a dict in the respose"
            assert product_data == {} or "id" not in product_data

        else:
            assert response.text == ""


def test_create_product(auth_headers):

    payload = {
        "title": "Test Product",
        "price": 10.99,
        "description": "Test description",
        "image": "https://i.pravatar.cc",
        "category": "electronics"
    }

    response = create_product(payload, headers=auth_headers)
    assert response.status_code == 201, "Create Product: Status code not 201"
    data = safe_json(response)
    assert data is not None, "Create Product: expected a json response" #assert that product_data can be safely converted to json
    assert isinstance(data, dict), "Create Product: Expected a dict in the response"
    assert data["title"] == payload["title"], "Create Product: Title does not match what was entered"

    validate_write_response(data, payload) #helper function in utils/validators.py#


def test_update_product(auth_headers):

    payload = {
        "id": 55,
        "title": "Test Product Updated",
        "price": 99.99,
        "description": "Test description updated",
        "image": "https://i.pravatar.cc/updated",
        "category": "home_goods"
    }

    response = update_product(44, payload, headers=auth_headers)
    assert response.status_code == 200
    data = safe_json(response)
    assert data is not None, "Update Product: expected a json response" #assert that product_data can be safely converted to json
    assert isinstance(data, dict)
    assert data["title"] == payload["title"]

    validate_write_response(data, payload) #helper function in utils/validators.py#

def test_delete_product(auth_headers):

    response = delete_product(44, headers=auth_headers)
    assert response.status_code ==  200



def test_product_e2e_workflow(auth_headers):

    #arrange - define the payload
    test_payload = {
        "title": "Test Product - E2E",
        "price": 1099.99,
        "description": "Test description - E2E",
        "image": "https://i.pravatar.cc/E2E",
        "category": "E2E"
    }

    #Lifecycle step: create a product, extract the ID returned by the API
    response = create_product(test_payload, headers=auth_headers)
    assert response.status_code == 201, "Create Product: status code not 201"
    returned_data = safe_json(response) #safe_json is a helper function. Returns None if the response returns a non-JSON response.
    assert returned_data is not None, "Create Product: expected JSON response but got none"
    assert isinstance(returned_data, dict)
    assert returned_data["title"] == test_payload["title"], "Create Product: Product title returned does not match title used"
    reference_id = returned_data["id"] #extract the ID that will be used for the get, update, and delete tests.
    validate_write_response(returned_data, test_payload) #helper function in utils/validators.py#


    #Lifecycle step: get the product (using the ID returned from create product)
    response_get = get_product_by_id(reference_id, headers=auth_headers)
    assert response_get.status_code == 200
    product_data = safe_json(response_get)
    #commenting out the json validation step below as the mocked api does not consistently return a json response
    #assert product_data is not None, "Get product by id: Expected JSON response but got none"
    if product_data is None:
        pytest.skip("GET after POST returned empty body — known FakeStoreAPI inconsistency")
        assert isinstance(product_data, dict)
        assert product_data["id"] == reference_id, "Get product by id: returned a different product ID than requested"
        validate_product(product_data)

    #Lifecycle step: update product, using the extracted ID
    updated_payload = test_payload.copy()
    updated_payload["title"] = "Test Product - E2E - Updated"
    updated_payload["price"] = 2199.98
    updated_payload["description"] = "Updated Test description - E2E"
    updated_payload["category"] = "E2E_updated"

    response = update_product(reference_id, updated_payload, headers=auth_headers)
    assert response.status_code == 200, "Update Product: status code not 200"
    returned_data = safe_json(response)
    assert returned_data is not None, "Update Product: expected JSON response but got none"
    assert isinstance(returned_data, dict)
    assert returned_data["id"] == reference_id, "Update Product: product id mismatch"
    validate_write_response(returned_data, updated_payload) #helper function in utils/validators.py#

    #validating the updated product
    response_get = get_product_by_id(reference_id, headers=auth_headers)
    assert response_get.status_code == 200
    product_data = safe_json(response_get)
    #commenting out the json validation step below as the mocked api does not consistently return a json response
    #assert product_data is not None, "Get product by id: Expected JSON response but got none"
    if product_data is None:
        pytest.skip("GET after UPDATE returned empty body — known FakeStoreAPI inconsistency")
        assert isinstance(product_data, dict)
        assert product_data["id"] == reference_id, "Get product by id: returned a different product ID than requested"
        validate_product(product_data)
        assert product_data["title"] == updated_payload["title"]
        assert product_data["price"] == updated_payload["price"]
        assert product_data["description"] == updated_payload["description"]
        assert product_data["category"] == updated_payload["category"]

    #act - delete the product
    response = delete_product(reference_id, headers=auth_headers)
    assert response.status_code ==  200

