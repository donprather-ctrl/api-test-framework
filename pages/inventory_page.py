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
        self.remove_buttons = page.locator("[data-test*='remove']")

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

    def sort_by_price_low_to_high(self):
        """Sort the inventory by price from lowest to highest."""
        self.page.locator("[data-test='product-sort-container']").select_option("lohi")

    def get_prices(self) -> list:
        """Return all product prices on the page as a list of floats."""
        price_elements = self.page.locator("div.inventory_item_price").all()
        prices = []
        for element in price_elements:
            price_text = element.inner_text()          # e.g. "$7.99"
            price = float(price_text.replace("$", "")) # e.g. 7.99
            prices.append(price)
        return prices
    
    def remove_first_item_from_cart(self):
        """Click the Remove button on the first product on the inventory page
        that contains the remove functionality.
        """
        self.remove_buttons.first.click()
    
    def expect_cart_is_empty(self):
        """Assert the cart badge is not visible (cart is empty)."""
        expect(self.cart_badge).not_to_be_visible()

    def click_cart_icon(self):
        """Click the cart icon to navigate to the cart page."""
        self.cart_badge.click()

    def expect_inventory_page_loaded(self):
        """Assert that inventory page loads successfully."""
        expect(self.page).to_have_url(self.URL)
        