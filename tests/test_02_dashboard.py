import pytest
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_dashboard_counts(driver):

    wait = WebDriverWait(driver, 30)

    driver.get("https://health-claim-ui-prod.artivatic.ai/auth/login")

    # ---------- LOGIN ----------
    wait.until(EC.element_to_be_clickable((By.ID, "empId"))).send_keys("furqan.shaikh@artivatic.ai")
    driver.find_element(By.ID, "password").send_keys("Furquan@dev1!")
    Select(driver.find_element(By.ID, "cn")).select_by_visible_text("India")
    driver.find_element(By.XPATH, "//button[contains(.,'LOGIN')]").click()

    # ---------- WAIT FOR DASHBOARD ----------
    wait.until(EC.url_contains("dashboard"))
    print("Login done")

    # ---------- GET DASHBOARD CARDS ----------
    cards = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//div[contains(@class,'upper_card')]")
    ))

    print("\nDashboard Metrics:\n")

    # ---------- EXTRACT LABEL + VALUE ----------
    for card in cards:
        try:
            full_text = card.text.strip()

            if "Advanced Filter" in full_text:
                continue

            lines = [line.strip() for line in full_text.split("\n") if line.strip()]

            label = None
            value = None

            for line in lines:
                # 🔥 Extract number using regex
                numbers = re.findall(r"\d+", line)

                if numbers:
                    value = "".join(numbers)   # join digits (handles commas etc.)
                else:
                    label = line

            if label and value:
                print(f"{label} : {value}")

        except Exception:
            continue

    assert len(cards) > 0, "No dashboard cards found"

    print("Execution completed successfully")
