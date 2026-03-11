import pytest
import logging
from utils.driver_factory import get_driver
from utils.screenshot_helper import take_screenshot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture: initializes a Chrome WebDriver before each test
    and quits it after (teardown).
    """
    driver = get_driver(headless=True)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture a screenshot automatically on test failure.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            test_name = item.nodeid.replace("/", "_").replace("::", "_")
            screenshot_path = take_screenshot(driver, test_name)
            logging.getLogger(__name__).warning(
                f"Test FAILED — screenshot saved: {screenshot_path}"
            )
