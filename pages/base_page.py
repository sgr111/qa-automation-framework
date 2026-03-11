from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all Page Objects. Contains common methods."""

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url: str):
        """Navigate to a URL."""
        self.driver.get(url)
        logger.info(f"Navigated to: {url}")

    def get_title(self) -> str:
        """Return the current page title."""
        return self.driver.title

    def get_url(self) -> str:
        """Return the current URL."""
        return self.driver.current_url

    def wait_for_element(self, by: By, locator: str):
        """Wait until an element is visible."""
        return self.wait.until(EC.visibility_of_element_located((by, locator)))

    def wait_for_element_clickable(self, by: By, locator: str):
        """Wait until an element is clickable."""
        return self.wait.until(EC.element_to_be_clickable((by, locator)))

    def is_element_present(self, by: By, locator: str) -> bool:
        """Check if an element is present on the page."""
        try:
            self.driver.find_element(by, locator)
            return True
        except Exception:
            return False
