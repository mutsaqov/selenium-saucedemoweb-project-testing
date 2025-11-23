import unittest
from selenium import webdriver
import os
from datetime import datetime
import sys

class BaseTest(unittest.TestCase):
    # 1. Setup Driver (Bisa dibuat dinamis untuk Chrome/Firefox)
    def setUp(self):
        self.driver = webdriver.Chrome()
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