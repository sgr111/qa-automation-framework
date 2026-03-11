import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def take_screenshot(driver, test_name: str) -> str:
    """
    Captures a screenshot and saves it to the screenshots/ directory.

    Args:
        driver: WebDriver instance
        test_name: Name of the test (used in filename)

    Returns:
        Path to the saved screenshot
    """
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{screenshots_dir}/{test_name}_{timestamp}.png"
    driver.save_screenshot(filename)
    logger.info(f"Screenshot saved: {filename}")
    return filename
