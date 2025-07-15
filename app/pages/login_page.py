from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from app.pages.dashboard_page import DashboardPage

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.NAME, "username")
        self.password_field = (By.NAME, "password")
        self.sign_in_button = (By.CSS_SELECTOR, "button[type='submit']")

    def login(self, email, password):
        self.driver.find_element(*self.email_field).send_keys(email)
        self.driver.find_element(*self.password_field).send_keys(password)
        self.driver.find_element(*self.sign_in_button).click()

        # ✅ Try alert in case of failure — ignore Timeout
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = Alert(self.driver)
            alert_text = alert.text
            alert.accept()
            raise Exception(f"Login failed - Alert Text: {alert_text}")
        except TimeoutException:
            pass  # No alert is fine — means login may have succeeded

        # ✅ Wait for dashboard header element to confirm success
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='header']/div[2]/div/button"))
        )

        return DashboardPage(self.driver)
