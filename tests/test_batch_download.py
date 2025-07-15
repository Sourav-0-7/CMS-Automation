import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_batch_download():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--start-maximized')
    
    # Set download directory
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    base_url = os.getenv('CMS_URL', 'http://54.218.101.86:9000/login')
    email = os.getenv('CMS_USERNAME', 'admin@qualityedgar.com')
    password = os.getenv('CMS_PASSWORD', 'password')

    try:
        from app.pages.login_page import LoginPage
        from app.pages.documents_page import DocumentsPage
        
        print(f"Navigating to: {base_url}")
        driver.get(base_url)
        login_page = LoginPage(driver)
        login_page.login(email, password)
        print(f"Logged in, current URL: {driver.current_url}")
        
        documents_page = DocumentsPage(driver)
        documents_page.batch_download_all()
        
        # Check for downloaded file with a loop
        max_wait = 60  # Total wait time in seconds
        for i in range(max_wait // 5):
            time.sleep(5)  # Check every 5 seconds
            downloaded_files = [f for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
            if downloaded_files:
                print(f"Download successful: {downloaded_files}")
                print("Batch Download: SUCCESS")
                break
        else:
            print("No files downloaded after waiting")
            print("Batch Download: FAILED - No download detected")
            driver.save_screenshot("batch_download_failure.png")
            raise Exception("No download detected after 60 seconds")
        
    except Exception as e:
        print(f"Batch Download: FAILED - {str(e)} - Page Title: {driver.title} - URL: {driver.current_url}")
        driver.save_screenshot("batch_download_failure.png")
    finally:
        driver.quit()

if __name__ == '__main__':
    test_batch_download()