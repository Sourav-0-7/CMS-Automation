import os
import sys
import logging
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Ensure parent directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Logging config
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def test_login():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Maximize the window for visibility
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    base_url = os.getenv('CMS_URL', 'http://54.218.101.86:9000/login')
    email = os.getenv('CMS_USERNAME', 'admin@qualityedgar.com')
    password = os.getenv('CMS_PASSWORD', 'password')  # Corrected spelling here

    logger.info(f"Starting test with URL: {base_url}, Email: {email}")

    try:
        logger.info("Running login test...")
        from app.cms_actions import perform_login
        perform_login(driver, base_url, email, password)
        print("Login Test: PASSED")
    except Exception as e:
        print(f"Login Test FAILED - {str(e)}")
        traceback.print_exc()  # Full traceback for debugging
        driver.save_screenshot("login_failure.png")
    finally:
        driver.quit()

if __name__ == '__main__':
    test_login()
