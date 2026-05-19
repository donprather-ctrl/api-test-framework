# utils/data_loader.py

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "test_data" 

def load(filename: str) -> dict | list:
    """
    Load test data from a JSON file in the test_data/ directory.
    
    Usage:
        data = load("users.json")
        payload = data["create_valid_user"]
    """
    
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Test data file not found: {path}")
    with open(path) as f:
        return json.load(f)