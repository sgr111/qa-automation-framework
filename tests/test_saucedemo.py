import pytest
import csv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage


# ─────────────────────────────────────────
# Helper: load test data from CSV
# ─────────────────────────────────────────

def load_users_from_csv():
    """Read user credentials from test_data/users.csv"""
    data = []
    csv_path = os.path.join(os.path.dirname(__file__), "..", "test_data", "users.csv")
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((row["username"], row["password"], row["expected_result"]))
    return data


# ─────────────────────────────────────────
# Test Suite: Login
# ─────────────────────────────────────────

class TestSaucedemoLogin:
    """Tests for Saucedemo login functionality."""

    @pytest.mark.smoke
    def test_valid_login(self, driver):
        """Verify standard user can log in successfully."""
        page = LoginPage(driver)
        page.open()
        page.login("standard_user", "secret_sauce")
        assert "inventory" in driver.current_url, \
            "Login failed — not redirected to inventory page"
        print("✅ Valid login successful")

    @pytest.mark.smoke
    def test_login_page_title(self, driver):
        """Verify login page title is correct."""
        page = LoginPage(driver)
        page.open()
        assert "Swag Labs" in driver.title, \
            f"Unexpected title: {driver.title}"

    @pytest.mark.regression
    def test_locked_out_user_cannot_login(self, driver):
        """Verify locked out user sees error message."""
        page = LoginPage(driver)
        page.open()
        page.login("locked_out_user", "secret_sauce")
        assert page.is_error_displayed(), \
            "Expected error message for locked out user"
        assert "locked out" in page.get_error_message().lower(), \
            f"Unexpected error: {page.get_error_message()}"
        print("✅ Locked out user correctly blocked")

    @pytest.mark.regression
    def test_invalid_credentials_show_error(self, driver):
        """Verify invalid credentials show error message."""
        page = LoginPage(driver)
        page.open()
        page.login("wrong_user", "wrong_pass")
        assert page.is_error_displayed(), \
            "Expected error message for invalid credentials"
        print(f"✅ Error shown: {page.get_error_message()}")

    @pytest.mark.regression
    def test_empty_username_shows_error(self, driver):
        """Verify empty username shows validation error."""
        page = LoginPage(driver)
        page.open()
        page.login("", "secret_sauce")
        assert page.is_error_displayed(), \
            "Expected error for empty username"

    @pytest.mark.regression
    def test_empty_password_shows_error(self, driver):
        """Verify empty password shows validation error."""
        page = LoginPage(driver)
        page.open()
        page.login("standard_user", "")
        assert page.is_error_displayed(), \
            "Expected error for empty password"

    @pytest.mark.regression
    @pytest.mark.parametrize("username,password,expected", load_users_from_csv())
    def test_login_data_driven(self, driver, username, password, expected):
        """Data driven test: verify login outcomes from CSV file."""
        page = LoginPage(driver)
        page.open()
        page.login(username, password)
        if expected == "success":
            assert "inventory" in driver.current_url, \
                f"Expected successful login for '{username}'"
            print(f"✅ '{username}' logged in successfully")
        else:
            assert page.is_error_displayed(), \
                f"Expected error for '{username}'"
            print(f"✅ '{username}' correctly rejected")


# ─────────────────────────────────────────
# Test Suite: Products
# ─────────────────────────────────────────

class TestSaucedemoProducts:
    """Tests for Saucedemo products page."""

    @pytest.fixture(autouse=True)
    def login(self, driver):
        """Auto-login before each test in this class."""
        page = LoginPage(driver)
        page.open()
        page.login("standard_user", "secret_sauce")

    @pytest.mark.smoke
    def test_products_page_loads(self, driver):
        """Verify products page loads after login."""
        page = ProductsPage(driver)
        assert page.get_page_title() == "Products", \
            f"Expected 'Products', got: '{page.get_page_title()}'"

    @pytest.mark.regression
    def test_products_count_is_six(self, driver):
        """Verify exactly 6 products are displayed."""
        page = ProductsPage(driver)
        assert page.get_product_count() == 6, \
            f"Expected 6 products, got: {page.get_product_count()}"

    @pytest.mark.regression
    def test_add_product_to_cart(self, driver):
        """Verify adding a product updates cart badge."""
        page = ProductsPage(driver)
        page.add_first_product_to_cart()
        assert page.get_cart_count() == 1, \
            f"Expected cart count 1, got: {page.get_cart_count()}"
        print("✅ Product added to cart successfully")

    @pytest.mark.regression
    def test_product_prices_are_positive(self, driver):
        """Verify all product prices are greater than zero."""
        page = ProductsPage(driver)
        prices = page.get_product_prices()
        for price in prices:
            assert price > 0, f"Invalid price found: {price}"
        print(f"✅ All {len(prices)} prices are valid: {prices}")

    @pytest.mark.regression
    def test_sort_products_low_to_high(self, driver):
        """Verify products can be sorted by price low to high."""
        page = ProductsPage(driver)
        page.sort_products("lohi")
        prices = page.get_product_prices()
        assert prices == sorted(prices), \
            f"Prices not sorted low to high: {prices}"
        print(f"✅ Prices sorted correctly: {prices}")


# ─────────────────────────────────────────
# Test Suite: End-to-End Checkout
# ─────────────────────────────────────────

class TestSaucedemoCheckout:
    """End-to-end checkout flow tests."""

    @pytest.fixture(autouse=True)
    def login(self, driver):
        """Auto-login before each test."""
        page = LoginPage(driver)
        page.open()
        page.login("standard_user", "secret_sauce")

    @pytest.mark.smoke
    def test_complete_checkout_flow(self, driver):
        """
        E2E test: Login → Add product → Cart → Checkout → Complete.
        This is the most important test for resume demonstration.
        """
        # Step 1: Add product to cart
        products = ProductsPage(driver)
        products.wait_for_element(*ProductsPage.PRODUCT_ITEMS)
        products.add_product_by_name("Sauce Labs Backpack")
        assert products.get_cart_count() == 1, \
            f"Expected cart count 1, got: {products.get_cart_count()}"

        # Step 2: Go to cart
        products.go_to_cart()

        # Wait for cart URL and container
        WebDriverWait(driver, 10).until(EC.url_contains("cart"))
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cart_contents_container"))
        )

        cart = CartPage(driver)
        items = driver.find_elements(By.CSS_SELECTOR, ".cart_item")
        assert len(items) == 1, f"Expected 1 cart item, got {len(items)}"
        assert "Sauce Labs Backpack" in cart.get_cart_item_names()

        # Step 3: Checkout
        cart.click_checkout()
        cart.fill_checkout_info("John", "Doe", "12345")

        # Step 4: Finish order
        cart.click_finish()
        assert cart.is_order_complete(), \
            "Order completion message not shown"
        print(f"✅ E2E checkout complete: {cart.get_order_complete_header()}")

    @pytest.mark.regression
    def test_cart_is_empty_initially(self, driver):
        """Verify cart is empty right after login."""
        page = ProductsPage(driver)
        assert page.get_cart_count() == 0, \
            "Cart should be empty after fresh login"
