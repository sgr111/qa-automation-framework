from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time
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

    def _dismiss_popups(self):
        """Dismiss any browser popups or overlays via JavaScript."""
        try:
            self.driver.execute_script("""
                document.querySelectorAll('div[role="dialog"]').forEach(e => e.remove());
                document.querySelectorAll('.modal').forEach(e => e.remove());
            """)
        except Exception:
            pass

    def get_cart_item_count(self) -> int:
        """Return number of items in cart."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.CART_ITEMS)
            )
            return len(self.driver.find_elements(*self.CART_ITEMS))
        except Exception:
            return 0

    def get_cart_item_names(self) -> list:
        """Return list of item names in cart."""
        elements = self.driver.find_elements(*self.CART_ITEM_NAMES)
        return [e.text for e in elements]

    def click_checkout(self):
        """Click the Checkout button using JS to bypass popups."""
        self._dismiss_popups()
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("cart")
        )
        btn = self.driver.find_element(*self.CHECKOUT_BUTTON)
        self.driver.execute_script("arguments[0].click();", btn)
        logger.info("Clicked Checkout")

    def fill_checkout_info(self, first: str, last: str, postal: str):
        """Fill checkout form using React-compatible JS input setter."""
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("checkout-step-one")
        )
        self._dismiss_popups()
        time.sleep(0.5)

        # React requires native input value setter + input event to register values
        self.driver.execute_script("""
            function setReactValue(el, value) {
                var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(el, value);
                el.dispatchEvent(new Event('input', { bubbles: true }));
            }
            setReactValue(document.getElementById('first-name'), arguments[0]);
            setReactValue(document.getElementById('last-name'), arguments[1]);
            setReactValue(document.getElementById('postal-code'), arguments[2]);
        """, first, last, postal)

        time.sleep(0.5)
        self._dismiss_popups()
        btn = self.driver.find_element(*self.CONTINUE_BUTTON)
        self.driver.execute_script("arguments[0].click();", btn)
        logger.info(f"Filled checkout info: {first} {last}, {postal}")

    def click_finish(self):
        """Click Finish button to complete order."""
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("checkout-step-two")
        )
        self._dismiss_popups()
        btn = self.driver.find_element(*self.FINISH_BUTTON)
        self.driver.execute_script("arguments[0].click();", btn)
        logger.info("Clicked Finish — order placed")

    def get_order_complete_header(self) -> str:
        """Return order confirmation header text."""
        try:
            return self.wait_for_element(*self.COMPLETE_HEADER).text
        except Exception:
            return ""

    def is_order_complete(self) -> bool:
        """Check if order completion message is shown."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("checkout-complete")
            )
            return self.is_element_present(*self.COMPLETE_HEADER)
        except Exception:
            return False
