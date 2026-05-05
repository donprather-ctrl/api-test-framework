#tests/test_ui_interaction.py

from playwright.sync_api import Page, expect
import pytest

@pytest.mark.ui
@pytest.mark.smoke
def test_login_valid_credentials(page: Page):
    """
    Validates that a user can log in with valid credentials.
    Verifies the products page loads after successful login.
    """
    # Act
    page.goto("https://www.saucedemo.com")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    # Assert
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.get_by_text("Products")).to_be_visible()


@pytest.mark.ui
@pytest.mark.smoke
def test_login_invalid_credentials(page: Page):
    """
    Validates that login fails with invalid credentials.
    Verifies an appropriate error message is displayed.
    """
    # Act
    page.goto("https://www.saucedemo.com")
    page.get_by_placeholder("Username").fill("invalid_user")
    page.get_by_placeholder("Password").fill("wrong_password")
    page.get_by_role("button", name="Login").click()

    # Assert
    expect(page.get_by_text("Epic sadface: Username and password do not match")).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
def test_add_product_to_cart(page: Page):
    """
    Validates that a user can add a product to the cart.
    Verifies cart count updates after adding an item.
    """
    # Arrange — log in first
    page.goto("https://www.saucedemo.com")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    # Act
    page.get_by_role("button", name="Add to cart").first.click()

    # Assert
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")