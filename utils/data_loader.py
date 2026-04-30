#utils/data_loader.py

import json
from pathlib import Path
from config.config import TEST_DATA_PATH

def load_test_data():
    with open(TEST_DATA_PATH) as f:
        return json.load(f)

