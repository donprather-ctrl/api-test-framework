# tests/test_ui_search.py

from playwright.sync_api import Page, expect
import pytest
from pages.cart_page import CartPage
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
    inventory_page.expect_cart_count(1), "Cart badge did not update to 1 after adding an item"


@pytest.mark.ui
@pytest.mark.regression
def test_sort_products_by_price_low_to_high(authenticated_page):
    """Inventory page can be sorted by price from lowest to highest."""

    inventory_page = InventoryPage(authenticated_page)
    inventory_page.navigate() # Navigate to inventory page directly since we're already authenticated
    inventory_page.sort_by_price_low_to_high()
    prices = inventory_page.get_prices()
    assert prices == sorted(prices), "Products are not sorted by price low to high"


@pytest.mark.ui
@pytest.mark.regression
def test_remove_item_from_cart(authenticated_page): 
    """Authenticated user can remove an item from the cart."""
    inventory_page = InventoryPage(authenticated_page)
    inventory_page.navigate() 
    inventory_page.add_first_item_to_cart()# Ensure there's an item in the cart to remove
    inventory_page.expect_cart_count(1), "During setup cart badge did not update to 1 after adding an item"
    inventory_page.remove_first_item_from_cart()
    inventory_page.expect_cart_is_empty()


@pytest.mark.ui
@pytest.mark.regression
def test_view_cart_not_empty(authenticated_page):
    """Authenticated user can view cart with items in it."""
    inventory_page = InventoryPage(authenticated_page)
    inventory_page.navigate() 
    inventory_page.add_first_item_to_cart()# Ensure there's an item in the cart to remove
    inventory_page.click_cart_icon()

    cart_page = CartPage(authenticated_page)
    cart_page.expect_cart_page_loaded()
    cart_page.expect_cart_count(1), "Cart badge does not show 1 item in cart on cart page"
    cart_page.click_continue_shopping()

    inventory_page.expect_inventory_page_loaded()
    inventory_page.expect_cart_count(1), "Cart badge does not show 1 item in cart after navigating back from cart page"