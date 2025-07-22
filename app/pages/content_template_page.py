from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, WebDriverException
import time

class ContentTemplate:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20) 

        # Locators
        self.content_template_tab = (By.XPATH, "//button[.//span[text()='Content Templates']]")
        self.create_new_button = (By.XPATH, "/html/body/div/div/div[3]/div/div/div[1]/div[1]/div/button[1]")
        self.template_name_input = (By.XPATH, "//input[@name='template_name'] | //input[contains(@id, 'r1j')]")
        self.create_button = (By.XPATH, "/html/body/div[2]/div[3]/div[3]/div/button[2]")

        # Dropdown Triggers (MUI combobox role)
        self.registrant_dropdown_trigger = (By.XPATH, "//label[text()='Registrant']/following-sibling::div//div[@role='combobox']")
        self.filing_type_dropdown_trigger = (By.XPATH, "//label[text()='Filing Type']/following-sibling::div//div[@role='combobox']")
        self.style_template_dropdown_trigger = (By.XPATH, "//label[text()='Style Template']/following-sibling::div//div[@role='combobox']")

        # Generic locator for the dropdown listbox (ul with role='listbox' within a common MUI popover)
        self.generic_mui_listbox_container = (By.XPATH, 
            "//div[contains(@class, 'MuiPopover-paper')]//ul[@role='listbox'] | //ul[contains(@class, 'MuiMenu-list') and @role='listbox'] | //ul[@role='listbox']"
        )
        # Locator for an option within any listbox
        self.option_text_locator = lambda text: (By.XPATH, f"//li[normalize-space()='{text}']")

    def open_content_template_modal(self):
        try:
            tab = self.wait.until(EC.element_to_be_clickable(self.content_template_tab))
            self.driver.execute_script("arguments[0].click();", tab)
        except TimeoutException:
            self.driver.save_screenshot("content_templates_tab_timeout.png")
            raise

        try:
            create_btn = self.wait.until(EC.element_to_be_clickable(self.create_new_button))
            self.driver.execute_script("arguments[0].click();", create_btn)
            self.wait.until(EC.visibility_of_element_located(self.template_name_input))
        except TimeoutException:
            self.driver.save_screenshot("create_new_button_timeout.png")
            raise
     
    def fill_template_form(self, name):
        try:
            template_name_input_elem = self.wait.until(EC.presence_of_element_located(self.template_name_input))
            template_name_input_elem.send_keys(name)
        except TimeoutException:
            self.driver.save_screenshot("template_name_input_timeout.png")
            raise

        self._select_mui_dropdown(self.registrant_dropdown_trigger, "ABC Investments", "Registrant")
        self._select_mui_dropdown(self.filing_type_dropdown_trigger, "N-CSR", "Filing Type")

        try:
            # Wait for Style Template dropdown to become enabled/clickable
            self.wait.until(EC.element_to_be_clickable(self.style_template_dropdown_trigger))
            self._select_mui_dropdown(self.style_template_dropdown_trigger, "new", "Style Template")
        except TimeoutException:
            self.driver.save_screenshot("style_template_disabled_timeout.png")
            raise
        except ElementClickInterceptedException:
             self.driver.save_screenshot("style_template_intercepted.png")
             raise


    def _select_mui_dropdown(self, trigger_locator, option_text, field_name):
        """Helper to interact with Material-UI Select/Dropdown components."""
        try:
            trigger_element = self.wait.until(EC.element_to_be_clickable(trigger_locator))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", trigger_element)
            trigger_element.click() 

            self.wait.until(EC.presence_of_element_located(self.generic_mui_listbox_container))
            self.wait.until(EC.visibility_of_element_located(self.generic_mui_listbox_container))

            option_element = self.wait.until(EC.element_to_be_clickable(self.option_text_locator(option_text)))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", option_element)
            option_element.click()

        except TimeoutException as e:
            self.driver.save_screenshot(f"{field_name.lower().replace(' ', '_')}_dropdown_timeout.png")
            
            # Debugging block: attempt to get listbox content on failure
            try:
                actual_listbox_element = self.driver.find_element(*self.generic_mui_listbox_container)
                try:
                    actual_listbox_element.find_element(*self.option_text_locator(option_text))
                except NoSuchElementException:
                    print(f"Debug: Option '{option_text}' NOT found in listbox HTML with locator {self.option_text_locator(option_text)}.")
            except NoSuchElementException:
                print(f"Debug: Could not find generic listbox for debugging with locator: {self.generic_mui_listbox_container}. It might not have appeared.")
            except WebDriverException as debug_e:
                print(f"Debug: WebDriverException during listbox inspection: {debug_e}")
            raise 
        except ElementClickInterceptedException:
            print(f"❗ Element click intercepted during {field_name} selection. An overlay might be present.")
            self.driver.save_screenshot(f"{field_name.lower().replace(' ', '_')}_dropdown_intercepted.png")
            raise
        except Exception as e:
            print(f"An unexpected error occurred during {field_name} selection: {e}")
            self.driver.save_screenshot(f"{field_name.lower().replace(' ', '_')}_unexpected_error.png")
            raise

    def submit(self):
        try:
            create_button = self.wait.until(EC.element_to_be_clickable(self.create_button))
            self.driver.execute_script("arguments[0].click();", create_button)
        except TimeoutException:
            print("❗ Timeout waiting for Create button.")
            self.driver.save_screenshot("create_button_timeout.png")
            raise