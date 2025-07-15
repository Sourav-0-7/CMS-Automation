from app.pages.login_page import LoginPage

def perform_login(driver, url, email, password):
    driver.get(url)
    login_page = LoginPage(driver)
    return login_page.login(email, password)  # ✅ RETURN the DashboardPage object
