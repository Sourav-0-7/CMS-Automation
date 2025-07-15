import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Add project root to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.cms_actions import perform_login

def test_dashboard():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    base_url = os.getenv('CMS_URL', 'http://54.218.101.86:9000/login')
    email = os.getenv('CMS_USERNAME', 'admin@qualityedgar.com')
    password = os.getenv('CMS_PASSWORD', 'password')

    try:
        print("🔄 Testing Dashboard...")
        dashboard = perform_login(driver, base_url, email, password)

        if dashboard.is_loaded():
            print("✅ Dashboard Test: PASSED")
        else:
            raise Exception("Dashboard did not load correctly.")

    except Exception as e:
        print(f"❌ Dashboard Test FAILED - {str(e)}")
        driver.save_screenshot("dashboard_failure.png")

    finally:
        driver.quit()

if __name__ == '__main__':
    test_dashboard()
