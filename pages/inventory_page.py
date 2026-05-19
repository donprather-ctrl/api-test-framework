# pages/inventory_page.py
from playwright.sync_api import Page, expect


class InventoryPage:
    """
    Page object representing the saucedemo inventory/products page.
    Encapsulates locators and actions available after login.
    """

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.add_to_cart_buttons = page.get_by_role("button", name="Add to cart")

    def navigate(self):
        """Navigate directly to the inventory page."""
        self.page.goto(self.URL)

    def add_first_item_to_cart(self):
        """Click the Add to cart button on the first product."""
        self.add_to_cart_buttons.first.click()

    def get_cart_count(self) -> str:
        """Return the current cart badge count as a string."""
        return self.cart_badge.inner_text()

    def expect_cart_count(self, count: int):
        """Assert the cart badge shows the expected count."""
        expect(self.cart_badge).to_have_text(str(count))