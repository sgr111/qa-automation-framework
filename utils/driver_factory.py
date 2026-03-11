from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import logging

logger = logging.getLogger(__name__)


def get_driver(browser: str = "chrome", headless: bool = True) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36")

    # Windows local path
    local_driver = r"C:\Users\Saurabh\chromedriver\chromedriver-win64\chromedriver.exe"

    if os.path.exists(local_driver):
        # Running locally on Windows
        service = Service(local_driver)
    else:
        # Running on GitHub Actions (Linux) — fix bad path from webdriver-manager
        raw_path = ChromeDriverManager().install()
        driver_path = raw_path.replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver")
        service = Service(driver_path)

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    logger.info(f"Chrome driver initialized (headless={headless})")
    return driver