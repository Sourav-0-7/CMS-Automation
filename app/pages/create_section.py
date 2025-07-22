# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.alert import Alert
# from app.pages.dashboard_page import DashboardPage

# class LoginPage:
#     def __init__(self, driver):
#         self.driver = driver
#         self.wait = WebDriverWait(driver, 20)
        
#         #Locators
#         self.first_document = (By.XPATH, "/html/body/div/div/div[3]/div/div/div[2]/div[1]/table/tbody/tr[1]/td[1]")
#         self.create_new_section_button = (By.XPATH, "/html/body/div/div/div[3]/div/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/button/svg/path")
#         self.section_name_input_field = (By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[1]")
#         self.master_page_style_dropdown = (By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[2]/div")
#         self.associate_to_series_dropdown = (By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[3]/div/div")
#         self.section_break_checkbox_switch = (By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[4]/label/span[1]/span[1]")
#         self.create_section = (By.XPATH, "/html/body/div[2]/div[3]/div[3]/div/button[2]")
        
#     def open_content_template_modal(self):
#         try:
#            print("✅ Clicked Content Templates tab.")  
            
            
#         except TimeoutException:
#              print("✅ Clicked Content Templates tab.")
                    
#     def select_all_documents(self):
#         self.driver.execute_script("window.scrollTo(0, 0);")
#         time.sleep(1)        

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CreateSectionPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def go_to_content_template_page(self):
        content_template_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Content Template']"))
        )
        content_template_button.click()

    def open_first_document(self):
        # Wait for the first table row and scroll it into view
        doc_element = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "(//tbody/tr)[1]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", doc_element)
        self.driver.execute_script("arguments[0].click();", doc_element)

    def create_section(self, section_name):
        # Click "Create Section"
        create_section_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Create Section')]"))
        )
        create_section_btn.click()

        # Input section name
        name_input = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='name']"))
        )
        name_input.clear()
        name_input.send_keys(section_name)

        # Click Save
        save_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Save')]"))
        )
        save_button.click()
