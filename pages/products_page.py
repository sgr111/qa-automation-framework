from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class ProductsPage(BasePage):
    """Page Object for Saucedemo Products Page."""

    # Locators
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".btn_inventory")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    CART_ICON = (By.CSS_SELECTOR, ".shopping_cart_link")
    SORT_DROPDOWN = (By.CSS_SELECTOR, ".product_sort_container")

    def get_page_title(self) -> str:
        """Return the products page title text."""
        try:
            return self.wait_for_element(*self.PAGE_TITLE).text
        except Exception:
            return ""

    def get_product_count(self) -> int:
        """Return total number of products displayed."""
        return len(self.driver.find_elements(*self.PRODUCT_ITEMS))

    def get_product_names(self) -> list:
        """Return list of all product names."""
        elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        return [e.text for e in elements]

    def get_product_prices(self) -> list:
        """Return list of all product prices as floats."""
        elements = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [float(e.text.replace("$", "")) for e in elements]

    def add_first_product_to_cart(self):
        """Click Add to Cart for the first product."""
        buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
        if buttons:
            buttons[0].click()
            logger.info("Added first product to cart")

    def add_product_by_name(self, product_name: str):
        """Add a specific product to cart by its name."""
        names = self.driver.find_elements(*self.PRODUCT_NAMES)
        for i, name in enumerate(names):
            if name.text == product_name:
                buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
                buttons[i].click()
                logger.info(f"Added '{product_name}' to cart")
                return
        raise ValueError(f"Product '{product_name}' not found")

    def get_cart_count(self) -> int:
        """Return number of items shown on cart badge."""
        try:
            return int(self.driver.find_element(*self.CART_BADGE).text)
        except Exception:
            return 0

    def go_to_cart(self):
        """Click the cart icon."""
        self.driver.find_element(*self.CART_ICON).click()
        logger.info("Navigated to cart")

    def sort_products(self, option: str):
        """Sort products. Options: 'az', 'za', 'lohi', 'hilo'"""
        from selenium.webdriver.support.ui import Select
        dropdown = self.driver.find_element(*self.SORT_DROPDOWN)
        Select(dropdown).select_by_value(option)
        logger.info(f"Sorted products by: {option}")
