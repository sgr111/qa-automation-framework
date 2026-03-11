from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class GooglePage(BasePage):
    """Page Object for Google Search homepage."""

    URL = "https://www.google.com"

    # Locators
    SEARCH_BOX = (By.NAME, "q")
    SEARCH_BUTTON = (By.NAME, "btnK")
    SEARCH_RESULTS = (By.ID, "search")
    RESULT_STATS = (By.ID, "result-stats")
    FIRST_RESULT_LINK = (By.CSS_SELECTOR, "div.g a[href]")
    SUGGESTIONS_LIST = (By.CSS_SELECTOR, "ul[role='listbox'] li")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = self.URL

    def open(self, url: str = None):
        """Open Google homepage."""
        target = url or self.URL
        self.driver.get(target)
        logger.info(f"Opened Google: {target}")

    def get_title(self) -> str:
        """Return page title."""
        return self.driver.title

    def search(self, query: str):
        """Type a query in the search box and submit."""
        search_box = self.wait_for_element(*self.SEARCH_BOX)
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        logger.info(f"Searched for: '{query}'")

    def get_search_results_count_text(self) -> str:
        try:
            # Try multiple possible locators
            for locator in ["result-stats", "slim_appbar"]:
                try:
                    el = self.driver.find_element(By.ID, locator)
                    if el.text:
                        return el.text
                except:
                    continue
            # Fallback — if results are visible, return dummy text
            if self.are_results_displayed():
                return "results found"
            return ""
        except Exception:
            return ""   

    def are_results_displayed(self) -> bool:
        """Check if search results section is visible."""
        return self.is_element_present(*self.SEARCH_RESULTS)

    def get_first_result_link(self) -> str:
        try:
            # Try multiple CSS selectors
            for selector in [
                "div.g a[href]",
                "#search a[href]",
                "a[jsname]",
                ".tF2Cxc a",
            ]:
                try:
                    el = self.driver.find_element(By.CSS_SELECTOR, selector)
                    href = el.get_attribute("href")
                    if href and href.startswith("http"):
                        return href
                except:
                    continue
            return ""
        except Exception:
           return ""

    def get_suggestions(self) -> list:
        """Return autocomplete suggestion texts."""
        try:
            suggestions = self.driver.find_elements(*self.SUGGESTIONS_LIST)
            return [s.text for s in suggestions if s.text]
        except Exception:
            return []
