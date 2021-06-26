import os
import pathlib

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from browser_utils import make_driver


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


if __name__ == '__main__':
    with make_driver(headless=not bool(os.getenv('DISABLE_HEADLESS'))) as driver:
        username, password = os.environ["USERNAME"], os.environ["PASSWORD"]
        authorize_at_ya(username=username, password=password, driver=driver)

        file_path = str(pathlib.Path("./map.geojson").resolve())
        map_js_code_str = import_geojson_to_ya(file_path=file_path, driver=driver)
        with open("map.html", "w") as f:
            f.write(map_js_code_str)
