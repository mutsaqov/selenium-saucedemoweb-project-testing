import unittest
from selenium import webdriver
import os
from datetime import datetime
import sys
import json
from pages.login_page import sauceDemoLoginPage
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

##---1: BASE TEST LOGGED IN---
class BaseTest(unittest.TestCase):

    # 1. Setup Driver (Bisa dibuat dinamis untuk Chrome/Firefox)
    def setUp(self):
        #0. CHROME OPTIONS
        options = webdriver.ChromeOptions()

        #Shutdown "Save Password" and "Password Leak Detection"
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "safebrowsing.enabled": False, # Turn Off safebrowsing
            "profile.default_content_setting_values.notifications": 2 # Blokir notifikasi
        }
        options.add_experimental_option("prefs", prefs)  

        # Argument for turning off another features that will be interupt automation process
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-save-password-bubble")
        options.add_argument("--no-sandbox") 
        options.add_argument("--disable-dev-shm-usage") 
        
        # Remove bar "Chrome is being controlled by automated test software"
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"Error saat start Chrome: {e}")
            raise e
    
        self.driver.maximize_window()

    # 2. Logika Screenshot on Failure
    def tearDown(self):
        
        # Jika sys.exc_info()[0] (tipe exception) BUKAN None, berarti ada kegagalan.
        test_failed = sys.exc_info()[0] is not None
        if test_failed:
            #create screenshots folder
            os.makedirs('screenshots')

            test_method_name = self._testMethodName 
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"screenshots/{test_method_name}_{timestamp}.png"

            # AMBIL SCREENSHOT
            self.driver.save_screenshot(file_name)
            print(f"!! TEST FAILED: Screenshots saved on {file_name}")

        self.driver.quit()

##---2: BASE TEST LOGGED IN (for all features after login)---
class BaseTestLoggedIn(BaseTest):
    def setUp(self):
        super().setUp()
        current_dir = os.path.dirname(__file__)
        data_path = os.path.join(current_dir, '..', 'data', 'users.json')

        with open(data_path, 'r') as f:
            data = json.load(f)
            valid_user = data['positive_cases'][0]
            username = valid_user['username']
            password = valid_user['password']           

        print(f"--- Running Positive Test: {username} ---")
        self.login_page = sauceDemoLoginPage(self.driver)
        self.login_page.open_page()
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_loginbtn()