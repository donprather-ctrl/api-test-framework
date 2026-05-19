# pages/login_page.py

from playwright.sync_api import Page, expect


class LoginPage:
    """
    Page object representing the saucedemo login page.
    Encapsulates all locators and actions for the login page
    so tests never interact with raw locators directly.
    """

    URL = "https://www.saucedemo.com"

    def __init__(self, page: Page):
        self.page = page
        # Locators — defined once here, used everywhere
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.locator(".error-message-container")

    def navigate(self):
        """Navigate to the login page."""
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        """Fill credentials and submit the login form."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self) -> str:
        """Return the visible error message text."""
        return self.error_message.inner_text()

    def expect_successful_login(self):
        """Assert that login succeeded and the inventory page loaded."""
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html")
        expect(self.page.get_by_text("Products")).to_be_visible()