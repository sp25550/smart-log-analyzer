import os
import time
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://127.0.0.1:5000"


def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    return driver


def wait_for_server(url, timeout=30):
    for _ in range(timeout):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return True
        except:
            time.sleep(1)
    return False


@pytest.fixture(scope="module")
def driver():
    assert wait_for_server(BASE_URL), "Flask server not running"
    driver = setup_driver()
    yield driver
    driver.quit()


def test_homepage_ui_elements(driver):
    driver.get(BASE_URL)

    assert driver.find_element(By.NAME, "logfile")
    assert driver.find_element(By.XPATH, "//button[contains(text(),'Analyze')]")