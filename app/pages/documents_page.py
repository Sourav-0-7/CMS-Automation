from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DocumentsPage:
    def __init__(self, driver):
        self.driver = driver

    def click_batch_download_button(self):
        batch_download_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='dashboard-container']/div/div[1]/div[1]/button[3]"))
        )
        batch_download_btn.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='dashboard-container']/div/div[2]/div[1]/div/div/button[5]"))
        )

    def select_all_documents(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        checkbox = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='dashboard-container']/div/div[2]/div[1]/table/thead/tr/th[1]/span/input"))
        )

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)

    def click_download_button(self, xpath, label):
        try:
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            btn.click()
            print(f"Clicked: {label}")
            time.sleep(5)
        except Exception as e:
            print(f"Failed to click '{label}': {str(e)}")

    def batch_download_all(self):
        try:
            self.click_batch_download_button()
            time.sleep(2)
            self.select_all_documents()
            time.sleep(1)

            # Perform all downloads in order
            self.click_download_button(
                "//*[@id='dashboard-container']/div/div[2]/div[1]/div/div/button[1]",
                "Download Selected"
            )

            self.click_download_button(
                "//*[@id='dashboard-container']/div/div[2]/div[1]/div/div/button[2]",
                "Web Ready PDF"
            )

            self.click_download_button(
                "//*[@id='dashboard-container']/div/div[2]/div[1]/div/div/button[3]",
                "Grayscale PDF"
            )

            self.click_download_button(
                "//*[@id='dashboard-container']/div/div[2]/div[1]/div/div/button[4]",
                "Download HTML"
            )

        finally:
            print("Closing browser after downloads...")
            self.driver.quit()
