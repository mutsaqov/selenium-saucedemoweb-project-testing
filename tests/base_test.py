import unittest
from selenium import webdriver
import os
from datetime import datetime
import sys
import json
import logging
from pages.login_page import sauceDemoLoginPage
from selenium.webdriver.chrome.service import Service

##---1: BASE TEST LOGGED IN---
class BaseTest(unittest.TestCase):

    # 1. Setup Driver (Manual Path)
    def setUp(self):
        #Logging setup
        self.config_logging()

        self.logger.info("=====================================")
        self.logger.info(f"STARTING TEST: {self._testMethodName}")
        self.logger.info("=====================================")
        
        
        # 0. CHROME OPTIONS
        options = webdriver.ChromeOptions()

        # Shutdown "Save Password" and "Password Leak Detection"
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "safebrowsing.enabled": False, # Turn Off safebrowsing
            "profile.default_content_setting_values.notifications": 2, # Blokir notifikasi
            "profile.password_manager_leak_detection": False,
        }
        options.add_experimental_option("prefs", prefs)  

        # Argument for turning off other features that interrupt automation
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-save-password-bubble")
        options.add_argument("--no-sandbox") 
        options.add_argument("--disable-dev-shm-usage") 
        options.add_argument("--disable-features=PasswordLeakDetection")
        
        
        # Remove bar "Chrome is being controlled by automated test software"
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        
        # Mencari file chromedriver.exe di folder utama project (satu level di atas folder tests)
        current_folder = os.path.dirname(os.path.abspath(__file__)) # Folder 'tests'
        project_root = os.path.dirname(current_folder)              # Folder Project Utama
        driver_path = os.path.join(project_root, "chromedriver.exe")

        # Cek apakah file driver benar-benar ada
        if not os.path.exists(driver_path):
            raise FileNotFoundError(f"ERROR: File chromedriver.exe tidak ditemukan di: {driver_path}")

        try:
            # Menggunakan Service dengan path manual
            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            self.logger.info(f"Error WHEN start Chrome: {e}")
            raise e
    
        self.driver.maximize_window()

    # 2. Logika Screenshot on Failure
    def tearDown(self):
        
        # Jika sys.exc_info()[0] (tipe exception) BUKAN None, berarti ada kegagalan.
        test_failed = sys.exc_info()[0] is not None
        if test_failed:
            #create screenshots folder if not exists
            if not os.path.exists('screenshots'):
                os.makedirs('screenshots')

            test_method_name = self._testMethodName 
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"screenshots/{test_method_name}_{timestamp}.png"

            # AMBIL SCREENSHOT
            try:
                self.driver.save_screenshot(file_name)
                self.logger.info(f"!! TEST FAILED: Screenshots saved on {file_name}")
            except:
                self.logger.info("FAILED TO TAKE SCREENSHOT")

        try:
            self.driver.quit()
        except:
            pass
        
    #logging function
    def config_logging(self):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        log_folder = os.path.join(project_root, 'logs')

        #Creating logging folder
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        log_file_path = os.path.join(log_folder, 'automation_test.log')
        #Format log
        log_formatter = logging.Formatter("%(asctime)s - %(levelname)s = %(message)s")
        
        #Logger Object
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        
        #Checking handler
        if not self.logger.handlers:
            #File handler
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(log_formatter)
            self.logger.addHandler(file_handler)
            
            #Console Handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_formatter)
            self.logger.addHandler(console_handler)

##---2: BASE TEST LOGGED IN (for all features after login)---
class BaseTestLoggedIn(BaseTest):
    def setUp(self):
        super().setUp()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, '..', 'data', 'users.json')

        with open(data_path, 'r') as f:
            data = json.load(f)
            # Mengambil data user pertama untuk login
            valid_user = data['positive_cases'][0]
            username = valid_user['username']
            password = valid_user['password']           

        self.logger.info(f"--- Running Positive Test: {username} ---")
        self.login_page = sauceDemoLoginPage(self.driver)
        self.login_page.open_page()
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_loginbtn()