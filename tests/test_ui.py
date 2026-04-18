import os
import time
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


BASE_URL = "http://127.0.0.1:5000"


# ---------- DRIVER SETUP ----------
def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver


# ---------- WAIT FOR FLASK ----------
def wait_for_server(url, timeout=20):
    for _ in range(timeout):
        try:
            requests.get(url)
            return True
        except:
            time.sleep(1)
    return False


# ---------- FIXTURE ----------
@pytest.fixture(scope="module")
def driver():
    assert wait_for_server(BASE_URL), "Flask server not running"
    driver = setup_driver()
    yield driver
    driver.quit()


# ---------- TEST FILE ----------
def test_homepage_ui_elements(driver):
    driver.get(BASE_URL)

    assert driver.find_element(By.NAME, "logfile")
    assert driver.find_element(By.XPATH, "//input[@type='submit']")


def test_upload_flow(driver):
    driver.get(BASE_URL)

    file_input = driver.find_element(By.NAME, "logfile")
    file_path = os.path.abspath("sample.log")

    file_input.send_keys(file_path)
    driver.find_element(By.XPATH, "//input[@type='submit']").click()

    time.sleep(2)

    page = driver.page_source.lower()
    assert "total" in page
    assert "logs" in page or "error" in page


def test_ui_rendering(driver):
    driver.get(BASE_URL)

    file_input = driver.find_element(By.NAME, "logfile")
    file_input.send_keys(os.path.abspath("sample.log"))

    driver.find_element(By.XPATH, "//input[@type='submit']").click()

    time.sleep(2)

    page = driver.page_source.lower()
    assert "warnings" in page
    assert "infos" in page


def test_invalid_file(driver):
    driver.get(BASE_URL)

    file_input = driver.find_element(By.NAME, "logfile")
    file_input.send_keys(os.path.abspath("invalid.log"))

    driver.find_element(By.XPATH, "//input[@type='submit']").click()

    time.sleep(2)

    # app should not crash
    assert "traceback" not in driver.page_source.lower()