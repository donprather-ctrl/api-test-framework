#utils/response_helpers.py

import requests


def safe_json(response):
    """
    Accepts an api response (call made using the requests library) object and returns
    none if the response object does not contain json that can be converted into a list or dict object.
    Returns the response object if it is valid json
    """

    if not response.text: #if the api does not return a text response
        return None

    try:
        return response.json()
    except ValueError:
        return None


import base64
import json

def decode_jwt_payload(token):
    """
    Decodes the payload section of a JWT token without verifying the signature.
    Returns the payload as a dict, or None if decoding fails.
    Useful for asserting token claims (expiry, user ID, username) in tests.
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload = parts[1]
        
        # JWT uses base64url encoding without padding characters.
        # Python's base64 decoder requires padding — add it back.
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += "=" * padding
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except Exception:
        return None