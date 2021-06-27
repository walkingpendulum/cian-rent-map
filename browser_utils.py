import time
from contextlib import contextmanager

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


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


def click_until_clicks(element: WebElement, timeout: int = 10) -> WebElement:
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            return element.click()
        except ElementNotInteractableException:
            time.sleep(0.5)

    return element.click()
