# tests/test_ui_search.py

from playwright.sync_api import Page, expect
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.mark.ui
@pytest.mark.smoke
def test_login_valid_credentials(page: Page):
    """Valid credentials navigate to the inventory page."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    login_page.expect_successful_login()


@pytest.mark.ui
@pytest.mark.smoke
def test_login_invalid_credentials(page: Page):
    """Invalid credentials display an error message."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("invalid_user", "wrong_password")
    assert "Username and password do not match" in login_page.get_error_message()


@pytest.mark.ui
@pytest.mark.regression
def test_add_product_to_cart(authenticated_page):
    """Authenticated user can add a product to the cart."""
    inventory_page = InventoryPage(authenticated_page)
    inventory_page.navigate()
    inventory_page.add_first_item_to_cart()
    inventory_page.expect_cart_count(1)