#pages/cart_page.py

from playwright.sync_api import Page, expect


class CartPage:
    """
    Page object representing the saucedemo cart page.
    Encapsulates locators and actions available on the cart page.
    """

    URL = "https://www.saucedemo.com/cart.html"


    def __init__(self, page: Page):
        self.page = page
        self.continue_shopping_button = page.locator("[data-test=\"continue-shopping\"]")
        self.cart_badge = page.locator(".shopping_cart_badge")
        

    def click_continue_shopping(self):
        """Click the Continue Shopping button to navigate back to the inventory page."""
        self.continue_shopping_button.click()

    def expect_cart_page_loaded(self):
        """Assert that cart page loads successfully."""
        expect(self.page).to_have_url("https://www.saucedemo.com/cart.html") 

    def get_cart_count(self) -> str:
        """Return the current cart badge count as a string."""
        return self.cart_badge.inner_text()

    def expect_cart_count(self, count: int):
        """Assert the cart badge shows the expected count."""
        expect(self.cart_badge).to_have_text(str(count))