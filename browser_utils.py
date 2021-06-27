from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver


@contextmanager
def make_driver(headless: bool = True, cleanup: bool = True) -> WebDriver:
    chrome_options = ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        yield driver
    finally:
        if cleanup:
            driver.quit()
