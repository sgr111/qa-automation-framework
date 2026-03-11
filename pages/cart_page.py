from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Page Object for Saucedemo Cart Page."""

    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    CART_ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    CART_ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, ".cart_button")

    # Checkout locators
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    COMPLETE_HEADER = (By.CSS_SELECTOR, ".complete-header")
    COMPLETE_TEXT = (By.CSS_SELECTOR, ".complete-text")

    def get_cart_item_count(self) -> int:
        """Return number of items in cart."""
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def get_cart_item_names(self) -> list:
        """Return list of item names in cart."""
        elements = self.driver.find_elements(*self.CART_ITEM_NAMES)
        return [e.text for e in elements]

    def click_checkout(self):
        """Click the Checkout button."""
        self.wait_for_element_clickable(*self.CHECKOUT_BUTTON).click()
        logger.info("Clicked Checkout")

    def fill_checkout_info(self, first: str, last: str, postal: str):
        """Fill checkout information form."""
        self.wait_for_element(*self.FIRST_NAME).send_keys(first)
        self.driver.find_element(*self.LAST_NAME).send_keys(last)
        self.driver.find_element(*self.POSTAL_CODE).send_keys(postal)
        self.driver.find_element(*self.CONTINUE_BUTTON).click()
        logger.info(f"Filled checkout info: {first} {last}, {postal}")

    def click_finish(self):
        """Click Finish button to complete order."""
        self.wait_for_element_clickable(*self.FINISH_BUTTON).click()
        logger.info("Clicked Finish — order placed")

    def get_order_complete_header(self) -> str:
        """Return order confirmation header text."""
        try:
            return self.wait_for_element(*self.COMPLETE_HEADER).text
        except Exception:
            return ""

    def is_order_complete(self) -> bool:
        """Check if order completion message is shown."""
        return self.is_element_present(*self.COMPLETE_HEADER)
