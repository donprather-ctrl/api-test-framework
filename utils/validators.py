#utils/validators.py#

#function description: accepts a single product (python dict) and validates the structure of the product data

def validate_product(product_data):

    assert isinstance(product_data, dict), "Product is not a dictionary"

    assert "id" in product_data, "Missing 'id'"
    assert isinstance(product_data["id"], int), "'id' is not int"

    assert "title" in product_data, "Missing 'title'"
    assert isinstance(product_data["title"], str), "'title' is not str"

    assert "price" in product_data, "Missing 'price'"
    assert isinstance(product_data["price"], (int, float)), "'price' is not numeric"

    assert "description" in product_data, "Missing 'description'"
    assert isinstance(product_data["description"], str), "'description' is not str"

    assert "category" in product_data, "Missing 'category'"
    assert isinstance(product_data["category"], str), "'category' is not str"

    assert "image" in product_data, "Missing 'image'"
    assert isinstance(product_data["image"], str), "'image' is not str"

    assert "rating" in product_data, "Missing 'rating'"
    rating = product_data["rating"]
    assert isinstance(rating, dict), "'rating' is not dict"

    assert "rate" in rating, "Missing 'rate'"
    assert isinstance(rating["rate"], (int, float)), "'rate' is not numeric"

    assert "count" in rating, "Missing 'count'"
    assert isinstance(rating["count"], int), "'count' is not int"


def validate_product_update_or_delete(data, payload):

    assert "id" in data, "id value not returned"
    assert isinstance(data["id"], int), "id is not an integer"

    assert "price" in data, "Missing price"
    assert data["price"] == payload["price"], "price does not match what was entered for this product"

    assert "description" in data, "Missing description"
    assert data["description"] == payload["description"], "Description does not match what was entered for this product"

    assert "image" in data, "Missing image uri"
    assert data["image"] == payload["image"], "Image does not match what was entered for this product"

    assert "category" in data, "Missing category"
    assert data["category"] == payload["category"], "Category does not match what was entered for this product"

    assert "title" in data, "Missing title"
    assert data["title"] == payload["title"], "Title does not match"
