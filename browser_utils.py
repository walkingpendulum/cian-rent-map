from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver


def make_driver(headless: bool = True) -> WebDriver:
    chrome_options = ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless")

    return webdriver.Chrome(options=chrome_options)
