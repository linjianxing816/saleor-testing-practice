import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://localhost:9000"
EMAIL = "admin@example.com"
PASSWORD = "admin"

SCREENSHOT_DIR = os.path.join(os.getcwd(), "screenshots")


def wait(driver, timeout=15):
    return WebDriverWait(driver, timeout)


def login_once(driver):
    """
    只在整个测试会话开始时登录一次。
    """
    driver.get(BASE_URL)

    email_input = wait(driver).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "input[name='email'], input[type='email']")
        )
    )

    password_input = driver.find_element(
        By.CSS_SELECTOR,
        "input[name='password'], input[type='password']"
    )

    email_input.clear()
    email_input.send_keys(EMAIL)

    password_input.clear()
    password_input.send_keys(PASSWORD)

    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    wait(driver).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(), 'Catalog') or contains(text(), 'Products') or contains(text(), 'Home')]")
        )
    )


@pytest.fixture(scope="session")
def driver():
    """
    整个测试文件只启动一个浏览器。
    """
    options = Options()
    options.add_argument("--start-maximized")

    # 不要开启 detach，否则测试结束后浏览器不会自动关闭
    # options.add_experimental_option("detach", True)

    driver = webdriver.Edge(options=options)
    driver.implicitly_wait(5)

    login_once(driver)

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试失败时自动截图。
    session 级 driver 需要从 item.funcargs 里取。
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)

        if driver:
            os.makedirs(SCREENSHOT_DIR, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"failed_{item.name}_{timestamp}.png"
            path = os.path.join(SCREENSHOT_DIR, filename)

            driver.save_screenshot(path)
            print(f"\n失败截图已保存：{path}")