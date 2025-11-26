from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class sauceDemoLoginPage:
    
    #LOCATORS
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    #CONSTRUCTOR
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    #ACTIONS
    def open_page(self):
        self.driver.get("https://www.saucedemo.com/")
        self.driver.maximize_window()

    def enter_username(self, username):
        element = self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        element.clear() 
        element.send_keys(username)

    def enter_password(self, password):
        element = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        element.clear()
        element.send_keys(password)

    def click_loginbtn(self):
        elemen = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        elemen.click()
    
    def get_error_message(self):
        elemen = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return elemen.text
    