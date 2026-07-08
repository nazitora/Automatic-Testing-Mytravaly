"""
WebDriver factory — creates and configures Chrome WebDriver instances.
Supports headed (default) and headless modes via HEADLESS=1 env var.
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.config import IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT


def get_driver() -> webdriver.Chrome:
    """
    Create and return a configured Chrome WebDriver instance.

    Set environment variable HEADLESS=1 to run in headless mode.
    """
    options = webdriver.ChromeOptions()
    options.page_load_strategy = "eager"

    # Headless mode toggle
    if os.environ.get("HEADLESS", "").strip() == "1":
        options.add_argument("--headless=new")

    # Stability & performance flags
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")

    # Suppress automation detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Initialize driver with webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Configure timeouts
    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    driver.maximize_window()

    return driver
