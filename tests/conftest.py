# tests/conftest.py

import pytest
from config.config import DEFAULT_USER, DEFAULT_PASSWORD
from api_client.auth_api import login_user
from playwright.sync_api import Browser

@pytest.fixture(scope="session")
def auth_headers():
    response = login_user(DEFAULT_USER, DEFAULT_PASSWORD)
    if response.status_code == 200:
        token = response.json()["accessToken"]
        return {"Authorization": f"Bearer {token}"}
    pytest.fail(f"Auth failed: {response.status_code} — {response.text}")



@pytest.fixture(scope="module")
def logged_in_state(browser, tmp_path_factory):
    """
    Logs into saucedemo once per module and saves browser state to a temp file.
    Subsequent tests load the saved state instead of repeating the login flow.
    """
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.saucedemo.com")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    state_path = tmp_path_factory.mktemp("state") / "logged_in.json"
    context.storage_state(path=str(state_path))
    context.close()
    return str(state_path)


@pytest.fixture
def authenticated_page(browser, logged_in_state):
    """
    Returns a page pre-loaded with saved login state.
    Each test gets a fresh page without repeating the login flow.
    """
    context = browser.new_context(storage_state=logged_in_state)
    page = context.new_page()
    yield page
    context.close()