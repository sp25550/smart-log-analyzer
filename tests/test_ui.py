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
def wait_for_server(url, timeout=25):
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


# ---------- TEST FILES SAFETY ----------
def get_file(name):
    path = os.path.abspath(name)
    assert os.path.exists(path), f"Missing file in workspace: {name}"
    return path


# ---------- TEST 1 ----------
def test_homepage_ui_elements(driver):
    driver.get(BASE_URL)

    assert driver.find_element(By.NAME, "logfile")

    # FIX: use BUTTON instead of input
    assert driver.find_element(By.TAG_NAME, "button")


# ---------- TEST 2 ----------
def test_upload_flow(driver):
    driver.get(BASE_URL)

    file_input = driver.find_element(By.NAME, "logfile")
    file_input.send_keys(get_file("sample.log"))

    driver.find_element(By.TAG_NAME, "button").click()

    time.sleep(2)

    page = driver.page_source.lower()
    assert "total" in page
    assert "errors" in page


# ---------- TEST 3 ----------
def test_ui_rendering(driver):
    driver.get(BASE_URL)

    file_input = driver.find_element(By.NAME, "logfile")
    file_input.send_keys(get_file("sample.log"))

    driver.find_element(By.TAG_NAME, "button").click()

    time.sleep(2)

    page = driver.page_source.lower()
    assert "warnings" in page
    assert "infos" in page


# ---------- TEST 4 ----------
def test_invalid_file(driver):
    driver.get(BASE_URL)

    file_input = driver.find_element(By.NAME, "logfile")

    # FIX: allow file existence safety
    invalid_path = get_file("invalid.log")
    file_input.send_keys(invalid_path)

    driver.find_element(By.TAG_NAME, "button").click()

    time.sleep(2)

    # app should not crash
    page = driver.page_source.lower()
    assert "traceback" not in page