import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://cian.ru")

    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login-btn"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(username)
    driver.find_element_by_xpath('//button[normalize-space()="Продолжить"]').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(password)
    driver.find_element_by_xpath('//button[normalize-space()="Войти"]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "user-avatar")))

    driver.get("https://www.cian.ru/rent/flat/favorites/")

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    favorites = soup.find_all('div', attrs={"data-name": "FavoriteEntity"})

    parsed_items = []
    for item in favorites:
        parsed_item = {
            'bargain_info': item.find('div', attrs={"data-name": "BargainTermsInfo"}).text,
            'address': item.find('div', attrs={"data-name": "Address"}).text,
            'main_title': item.find('div', attrs={"data-name": "MainTitle"}).text,
            "url": f"https://www.cian.ru{item.find('a', href=True).attrs['href']}",
        }
        parsed_items.append(parsed_item)

    for item in parsed_items:
        print(item)
