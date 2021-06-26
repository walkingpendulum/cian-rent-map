import dataclasses
import os
from typing import List, Tuple

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from browser_utils import make_driver


@dataclasses.dataclass
class Favorite:
    bargain_info: str
    address: str
    main_title: str
    url: str
    location: Tuple[float, float] = dataclasses.field(default=tuple())


def authorize_at_cian(username: str, password: str, driver: WebDriver) -> None:
    driver.get("https://cian.ru")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login-btn"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(username)
    driver.find_element_by_xpath('//button[normalize-space()="Продолжить"]').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "password"))).send_keys(password)
    driver.find_element_by_xpath('//button[normalize-space()="Войти"]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "user-avatar")))


def fetch_favorites_from_cian(driver: WebDriver) -> List[Favorite]:
    driver.get("https://cian.ru")

    username, password = os.environ["USERNAME"], os.environ["PASSWORD"]
    authorize_at_cian(username=username, password=password, driver=driver)

    driver.get("https://cian.ru/rent/flat/favorites/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "*[data-name='FavoriteEntity']")))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    favorites = soup.find_all('div', attrs={"data-name": "FavoriteEntity"})

    parsed_items = []
    for item in favorites:
        parsed_item = Favorite(
            bargain_info=item.find('div', attrs={"data-name": "BargainTermsInfo"}).text,
            address=item.find('div', attrs={"data-name": "Address"}).text,
            main_title=item.find('div', attrs={"data-name": "MainTitle"}).text,
            url=f"https://www.cian.ru{item.find('a', href=True).attrs['href']}",
        )
        parsed_items.append(parsed_item)

    return parsed_items


if __name__ == '__main__':
    with make_driver(headless=not bool(os.getenv('DISABLE_HEADLESS'))) as driver:
        parsed_items = fetch_favorites_from_cian(driver=driver)
