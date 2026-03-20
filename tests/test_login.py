import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_login(driver):

    driver.get("https://health-claim-ui-prod.artivatic.ai/auth/login")
    time.sleep(3)

    # ---------- USERNAME ----------
    driver.find_element(By.ID, "empId").send_keys("processingteam@insurer.com")

    # ---------- PASSWORD ----------
    driver.find_element(By.ID, "password").send_keys("Admin@123")

    # ---------- COUNTRY ----------
    Select(driver.find_element(By.ID, "cn")).select_by_visible_text("India")

    print("✅ India Selected")

    # ---------- LOGIN ----------
    driver.find_element(By.XPATH, "//button[contains(text(),'LOGIN')]").click()

    time.sleep(3)
    print("Current URL:", driver.current_url)

    # ---------- ASSERT ----------
    assert "dashboard" in driver.current_url, "❌ Login Failed"

    print("🎉 LOGIN TEST PASSED")