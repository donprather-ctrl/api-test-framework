#utils/response_helpers.py

import requests

#safe_json accepts an api response (call made using the requests library) object and returns
# returns None if the response object does not contain json that can be converted into a list or dict object.
# returns a list or dict object if the response object is valid json.
def safe_json(response):
    if not response.text: #if the api does not return a text response
        return None

    try:
        return response.json()
    except ValueError:
        return None
