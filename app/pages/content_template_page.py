from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ContentTemplate:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)  # Increased to 20 seconds for MUI rendering

        # Locators
        self.content_template_tab = (By.XPATH, "//button[.//span[text()='Content Templates']]")
        self.create_new_button = (By.XPATH, "/html/body/div/div/div[3]/div/div/div[1]/div[1]/div/button[1]")
        self.template_name_input = (By.XPATH, "//input[@name='template_name'] | //input[contains(@id, 'r1j')]")

        # MUI Dropdown containers (role="combobox")
        self.registrant_dropdown = (By.XPATH, "//div[@role='combobox' and contains(@class, 'MuiAutocomplete-root')]//input")
        self.filing_type_dropdown = (By.XPATH, "//div[@role='combobox' and contains(@class, 'MuiAutocomplete-root')][2]//input")
        self.style_template_dropdown = (By.XPATH, "//div[@role='combobox' and contains(@class, 'MuiAutocomplete-root')][3]//input")

        # Options inside MUI Autocomplete Popper (role="listbox")
        self.option = lambda text: (By.XPATH, f"//ul[@role='listbox']//li//span[text()='{text}']")

        self.create_button = (By.XPATH, "//button[normalize-space()='Create']")

    def open_content_template_modal(self):
        print("➡ Clicking on Content Templates tab...")
        tab = self.wait.until(EC.element_to_be_clickable(self.content_template_tab))
        self.driver.execute_script("arguments[0].click();", tab)

        print("➡ Clicking on Create New button...")
        create_btn = self.wait.until(EC.element_to_be_clickable(self.create_new_button))
        self.driver.execute_script("arguments[0].click();", create_btn)

    def fill_template_form(self, name):
        print("➡ Filling template name...")
        self.wait.until(EC.presence_of_element_located(self.template_name_input)).send_keys(name)

        print("➡ Selecting Registrant...")
        registrant = self.wait.until(EC.element_to_be_clickable(self.registrant_dropdown))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", registrant)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", registrant)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@role='listbox']"))).click()  # Ensure overlay is open
        self.wait.until(EC.element_to_be_clickable(self.option("ABC Investments"))).click()

        print("➡ Selecting Filing Type...")
        filing_type = self.wait.until(EC.element_to_be_clickable(self.filing_type_dropdown))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", filing_type)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", filing_type)
        self.wait.until(EC.element_to_be_clickable(self.option("N-CSR"))).click()

        print("➡ Selecting Style Template...")
        style_template = self.wait.until(EC.element_to_be_clickable(self.style_template_dropdown))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", style_template)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", style_template)
        self.wait.until(EC.element_to_be_clickable(self.option("new"))).click()

    def submit(self):
        print("➡ Clicking Create button...")
        create_button = self.wait.until(EC.element_to_be_clickable(self.create_button))
        self.driver.execute_script("arguments[0].click();", create_button)