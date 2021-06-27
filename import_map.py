import os
import pathlib
from typing import List

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from browser_utils import make_driver, click_until_clicks


def authorize_at_ya(username: str, password: str, driver: WebDriver) -> None:
    driver.get("https://passport.yandex.ru/auth")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "passp-field-login"))).send_keys(username)
    driver.find_element_by_xpath('//button[normalize-space()="Войти"]').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "passp-field-passwd"))).send_keys(password)
    driver.find_element_by_xpath('//button[normalize-space()="Войти"]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ProfileTile")))


def import_geojson_to_ya(file_path: str, driver: WebDriver) -> str:
    driver.get("https://yandex.ru/map-constructor/")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "button_id_import-button"))).click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))).send_keys(file_path)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "button_id_saveBtn"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "button_id_get-code-btn"))).click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "textarea_id_code-preview")))
    driver.execute_script("alert(document.getElementsByClassName('textarea_id_code-preview')[0].value)")
    alert: Alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    map_js_code = alert.text
    alert.accept()

    return map_js_code


def cleanup_rent_maps(driver: WebDriver, except_first_n: int = 1):
    driver.get("https://yandex.ru/map-constructor/")

    while True:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "map-selection-item")))
        map_selection_items: List[WebElement] = driver.find_elements_by_class_name("map-selection-item")
        rent_items = [item for item in map_selection_items if "rent 2021" in item.text]
        rent_items_to_delete = rent_items[except_first_n:]
        if not rent_items_to_delete:
            break

        for item in rent_items_to_delete:
            dropdown = item.find_element_by_class_name("map-selection-item__more-menu-dropdown")
            click_until_clicks(dropdown)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dropdown_switcher_button")))
            elements = driver.find_elements_by_class_name("menu__item")
            delete_button = next(e for e in elements if e.text == 'Удалить')
            delete_button.click()
            WebDriverWait(driver, 10).until(EC.alert_is_present()).accept()


if __name__ == '__main__':
    with make_driver(headless=not bool(os.getenv('DISABLE_HEADLESS'))) as driver:
        username, password = os.environ["USERNAME"], os.environ["PASSWORD"]
        authorize_at_ya(username=username, password=password, driver=driver)

        file_path = str(pathlib.Path("./map.geojson").resolve())
        map_js_code_str = import_geojson_to_ya(file_path=file_path, driver=driver)
        with open("map.html", "w") as f:
            f.write(map_js_code_str)

        cleanup_rent_maps(driver=driver, except_first_n=1)
