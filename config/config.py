import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
DEFAULT_USER = os.getenv("DEFAULT_USER")
DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD")
TEST_DATA_PATH = Path(__file__).parent.parent / "test_data" / "test_data.json"
