#api_client/products_api.py


import requests
from config.config import BASE_URL



def get_all_products(headers=None):

    return requests.get(f"{BASE_URL}/products", headers=headers)


def get_product_by_id(product_id, headers=None):
    return requests.get(
        f"{BASE_URL}/products/{product_id}",
        headers=headers
    )


def create_product(payload, headers=None):

    return requests.post(
        f"{BASE_URL}/products",
        json = payload,
        headers=headers

    )



def update_product(product_id, payload, headers=None):

    return requests.put(
        f"{BASE_URL}/products/{product_id}",
        json = payload,
        headers=headers

    )



def delete_product(product_id, headers=None):

    return requests.delete(
        f"{BASE_URL}/products/{product_id}",
        headers=headers
    )

