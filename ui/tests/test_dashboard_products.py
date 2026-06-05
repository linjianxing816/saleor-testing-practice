import os
import time
from datetime import datetime
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# =====================================
# 演示模式配置
# =====================================
DEMO_MODE = True
DEMO_DELAY = 1.0

def demo_pause(seconds=DEMO_DELAY):
    if DEMO_MODE:
        time.sleep(seconds)

# =====================================
# 基础等待
# =====================================
def wait(driver, timeout=15):
    return WebDriverWait(driver, timeout)

# =====================================
# Products 页面入口
# =====================================
def open_products_page(driver):
    products_url = "http://localhost:9000/dashboard/products/?asc=false&sort=date"

    current_url = driver.current_url.lower()
    body_text = driver.find_element(By.TAG_NAME, "body").text

    if "/dashboard/products" in current_url and "Products" in body_text:
        demo_pause(1)
        return

    driver.get(products_url)

    wait(driver).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//*[contains(text(), 'All products') or contains(text(), 'Search Products') or contains(text(), 'Products')]"
            )
        )
    )

    demo_pause(1)

# =====================================
# 创建产品弹窗操作
# =====================================
def open_create_product_modal(driver):
    create_button = wait(driver).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Create product') or contains(., 'Create Product') or contains(., 'Create')]"
            )
        )
    )

    demo_pause(0.8)
    create_button.click()

    modal_title = wait(driver).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[contains(text(), 'Create Product') or contains(text(), 'Create product') or contains(text(), 'Select a product type')]"
            )
        )
    )

    demo_pause(1.5)
    return modal_title

def close_create_product_modal(driver):
    """
    关闭 Create Product 弹窗。

    重点：
    不要等待 'Create Product' 消失，因为页面上的创建按钮本身也叫 Create Product。
    只等待弹窗内部特有内容消失，例如：
    Select a product type / Digital product / Physical product
    """

    demo_pause(1)

    back_button = wait(driver).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(., 'Back') or @aria-label='Back']"
            )
        )
    )

    back_button.click()

    # 这里只等待弹窗内部独有内容消失
    wait(driver).until(
        EC.invisibility_of_element_located(
            (
                By.XPATH,
                "//*[contains(text(), 'Select a product type') or contains(text(), 'Digital product') or contains(text(), 'Physical product')]"
            )
        )
    )

    demo_pause(0.8)

# =====================================
# 搜索输入框
# =====================================
def get_search_input(driver):
    return wait(driver).until(
        EC.visibility_of_element_located(
            (
                By.CSS_SELECTOR,
                "input[placeholder*='Search'], input[type='search'], input[name*='search']"
            )
        )
    )

# =====================================
# 截图功能
# =====================================
def save_screenshot(driver, name):
    screenshot_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")

    driver.save_screenshot(path)
    print(f"\n截图已保存：{path}")

    demo_pause(1)

# =====================================
# 测试函数
# =====================================

def test_products_entry_smoke_flow(driver):
    """
    只检查 Products 页面是否能正常进入。
    不点击 Create Product。
    """
    open_products_page(driver)

    page_text = driver.find_element(By.TAG_NAME, "body").text

    assert "Products" in page_text
    assert len(page_text.strip()) > 20


def test_products_page_fixed_elements_exist(driver):
    """
    检查 Products 页面固定元素是否存在。
    只检查按钮存在，不点击。
    """
    open_products_page(driver)

    page_text = driver.find_element(By.TAG_NAME, "body").text

    assert "Products" in page_text

    create_buttons = driver.find_elements(
        By.XPATH,
        "//button[contains(., 'Create') or contains(., 'Create Product') or contains(., 'Create product')]"
    )
    assert len(create_buttons) >= 1

    inputs = driver.find_elements(By.TAG_NAME, "input")
    assert len(inputs) >= 1

    assert len(page_text.strip()) > 20


def test_create_product_modal_screenshot(driver):
    """
    唯一负责弹窗的测试：
    打开 Products 页面 → 点击一次 Create Product → 截图 → 关闭一次弹窗
    """
    open_products_page(driver)

    open_create_product_modal(driver)

    save_screenshot(driver, "create_product_modal")

    close_create_product_modal(driver)

    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Products" in page_text


def test_products_page_scroll_to_bottom(driver):
    """
    页面滚动测试。
    不涉及 Create Product 弹窗。
    """
    open_products_page(driver)

    for y in range(0, 1200, 200):
        driver.execute_script(f"window.scrollTo(0, {y});")
        demo_pause(0.3)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    demo_pause(1)

    bottom_position = driver.execute_script(
        "return window.innerHeight + window.scrollY;"
    )
    page_height = driver.execute_script(
        "return document.body.scrollHeight;"
    )

    assert bottom_position <= page_height + 10


def test_products_search_input_can_type(driver):
    """
    搜索框输入测试。
    不涉及 Create Product 弹窗。
    """
    open_products_page(driver)

    search_input = get_search_input(driver)
    demo_pause(1)

    keyword = "test"

    search_input.clear()
    demo_pause(0.5)

    for ch in keyword:
        search_input.send_keys(ch)
        demo_pause(0.4)

    demo_pause(1)

    assert search_input.get_attribute("value") == keyword

    search_input.send_keys(Keys.CONTROL, "a")
    demo_pause(0.5)

    search_input.send_keys(Keys.BACKSPACE)
    demo_pause(1)