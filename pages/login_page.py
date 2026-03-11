from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Page Object for Saucedemo Login Page."""

    URL = "https://www.saucedemo.com"

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        """Open Saucedemo login page."""
        self.driver.get(self.URL)
        logger.info(f"Opened Saucedemo: {self.URL}")

    def login(self, username: str, password: str):
        """Enter credentials and click login."""
        self.wait_for_element(*self.USERNAME_INPUT).clear()
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        logger.info(f"Logged in with username: '{username}'")

    def get_error_message(self) -> str:
        """Return error message text if login fails."""
        try:
            return self.wait_for_element(*self.ERROR_MESSAGE).text
        except Exception:
            return ""

    def is_error_displayed(self) -> bool:
        """Check if error message is visible."""
        return self.is_element_present(*self.ERROR_MESSAGE)
