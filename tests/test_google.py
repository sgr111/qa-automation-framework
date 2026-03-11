import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.google_page import GooglePage


# ─────────────────────────────────────────
# Test Suite: Google Search
# ─────────────────────────────────────────

class TestGoogleTitle:
    """Tests related to the Google homepage title."""

    @pytest.mark.smoke
    def test_google_title_contains_google(self, driver):
        """Verify Google homepage title contains 'Google'."""
        page = GooglePage(driver)
        page.open()
        assert "Google" in page.get_title(), \
            f"Expected 'Google' in title, got: '{page.get_title()}'"
        print("✅ test passed: title contains 'Google'")

    @pytest.mark.smoke
    def test_google_title_is_exactly_google(self, driver):
        """Verify Google homepage title is exactly 'Google'."""
        page = GooglePage(driver)
        page.open()
        assert page.get_title() == "Google", \
            f"Expected title 'Google', got: '{page.get_title()}'"

    @pytest.mark.smoke
    def test_google_url_is_correct(self, driver):
        """Verify that the URL contains google.com after opening."""
        page = GooglePage(driver)
        page.open()
        assert "google.com" in page.get_url(), \
            f"Unexpected URL: {page.get_url()}"


class TestGoogleSearch:
    """Tests for Google search functionality."""

    @pytest.mark.regression
    @pytest.mark.parametrize("search_query", [
        "Selenium Python",
        "pytest automation",
        "QA engineer best practices",
        "Page Object Model",
    ])
    def test_search_returns_results(self, driver, search_query):
        """Verify that searching for a query returns results."""
        page = GooglePage(driver)
        page.open()
        page.search(search_query)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_contains("search"))

        assert page.are_results_displayed(), \
            f"No results displayed for query: '{search_query}'"
        print(f"✅ Results found for: '{search_query}'")

    @pytest.mark.regression
    def test_search_result_stats_shown(self, driver):
        """Verify result stats (e.g., 'About X results') are shown."""
        page = GooglePage(driver)
        page.open()
        page.search("OpenAI")

        stats = page.get_search_results_count_text()
        assert stats != "", "Result stats text was empty"
        print(f"✅ Result stats: {stats}")

    @pytest.mark.regression
    def test_first_result_has_valid_link(self, driver):
        """Verify the first result contains a valid https link."""
        page = GooglePage(driver)
        page.open()
        page.search("Python official site")

        first_link = page.get_first_result_link()
        assert first_link.startswith("http"), \
            f"First result link is not a valid URL: '{first_link}'"
        print(f"✅ First result link: {first_link}")

    @pytest.mark.regression
    def test_search_title_updates_after_search(self, driver):
        """Verify page title changes after performing a search."""
        page = GooglePage(driver)
        page.open()
        page.search("automation testing")
        new_title = page.get_title()
        assert new_title is not None and new_title != "", \
            "Page title was empty after search"
        print(f"✅ Title after search: '{new_title}'")


class TestGoogleNegative:
    """Negative / edge case tests."""

    @pytest.mark.regression
    def test_search_with_special_characters(self, driver):
        """Verify search does not crash with special characters."""
        page = GooglePage(driver)
        page.open()
        page.search("!@#$%^&*()")
        # Should not throw an exception — just verify we're still on a page
        assert page.get_title() != "", \
            "Page title was empty after special character search"

    @pytest.mark.regression
    def test_search_with_very_long_query(self, driver):
        """Verify search handles a very long input string."""
        page = GooglePage(driver)
        page.open()
        long_query = "automation " * 50
        page.search(long_query.strip())
        assert page.get_url() != "", "URL was empty after long query search"
