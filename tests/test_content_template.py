import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.pages.login_page import LoginPage
from app.pages.content_template_page import ContentTemplate

def test_create_content_template():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    base_url = os.getenv("CMS_URL", "http://54.218.101.86:9000/login")
    email = os.getenv("CMS_USERNAME", "admin@qualityedgar.com")
    password = os.getenv("CMS_PASSWORD", "password")

    try:
        print(f"Starting test on: {base_url}")
        driver.get(base_url)

        login_page = LoginPage(driver)
        login_page.login(email, password)

        print("✅ Logged in successfully")

        content_page = ContentTemplate(driver)
        content_page.open_content_template_modal()
        content_page.fill_template_form(name="AutoTemplate")
        content_page.submit()

        print("✅ Content Template Test PASSED")

    except Exception as e:
        print(f"❌ Content Template Test FAILED - {str(e)}")
        driver.save_screenshot("content_template_error.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_create_content_template()


