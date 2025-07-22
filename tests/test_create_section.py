import os
import sys
import logging
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Append parent path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Logging config
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def test_create_section():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    base_url = os.getenv('CMS_URL', 'http://54.218.101.86:9000/login')
    email = os.getenv('CMS_USERNAME', 'admin@qualityedgar.com')
    password = os.getenv('CMS_PASSWORD', 'password')

    logger.info(f"Starting test with URL: {base_url}, Email: {email}")

    try:
        logger.info("➡️ Logging in...")
        from app.cms_actions import perform_login
        perform_login(driver, base_url, email, password)

        logger.info("➡️ Starting section creation...")
        from app.pages.create_section import CreateSectionPage
        section_page = CreateSectionPage(driver)
        section_page.go_to_content_template_page()
        section_page.open_first_document()
        section_page.create_section("Test Section Name")

        logger.info("✅ Section Creation Test: PASSED")

    except Exception as e:
        logger.error(f"❌ Section Creation Test FAILED - {str(e)}")
        traceback.print_exc()
        driver.save_screenshot("create_section_failure.png")
    finally:
        driver.quit()

if __name__ == '__main__':
    test_create_section()
