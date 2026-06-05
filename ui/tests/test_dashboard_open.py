from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import DASHBOARD_URL, ADMIN_EMAIL, ADMIN_PASSWORD


def test_dashboard_login(driver):
    # 1. 打开 Saleor Dashboard 登录页
    driver.get(DASHBOARD_URL)

    # 2. 等待登录输入框加载完成
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    password_input = driver.find_element(By.NAME, "password")

    # 3. 输入账号密码
    email_input.clear()
    email_input.send_keys(ADMIN_EMAIL)

    password_input.clear()
    password_input.send_keys(ADMIN_PASSWORD)

    # 4. 点击登录按钮
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    login_button.click()

    # 5. 等待登录页的邮箱输入框消失，说明页面已经完成跳转
    WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located((By.NAME, "email"))
    )

    # 6. 断言当前页面已经不是登录页
    page_text = driver.find_element(By.TAG_NAME, "body").text.lower()

    assert "sign in" not in page_text