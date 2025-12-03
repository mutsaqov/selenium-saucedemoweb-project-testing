import unittest
from selenium import webdriver
import pytest
import sys
import os
# Trik agar Python bisa membaca folder 'pages' (kadang error path di Windows)
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pages.login_page import sauceDemoLoginPage
from pages.inventory_page import sauceDemoInventoryPage
from tests.base_test import BaseTest
import json
import os
from ddt import ddt, data


# --- HELPER FUNCTION JSON ---
def load_testdata(case_type):
    #path file test script
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, '..', 'data', 'users.json')

    with open(data_path, 'r') as f:
        data = json.load(f)
        # Return key from list (ex: 'negative_cases')
        return data.get(case_type, [])

#--- TEST CASES CLASS ----
@ddt
class TestLoginSeparated(BaseTest):

    def setUp(self):
        super().setUp()
        self.login_page = sauceDemoLoginPage(self.driver)
        self.login_page.open_page()
        print("1. Open SauceDemo web...")
        self.inventory_page = sauceDemoInventoryPage(self.driver)
        
    # 1. --- POSITIVE CASE FUNCTION ---
    @data(*load_testdata('positive_cases')) #<--- CALL Helper Function

    def test_01_positive_login(self, data_set):
        """LGN-01: Verify successful login with valid standard_user credentials. """
        #Get the value, since data entry as a single dictionary
        username = data_set['username']
        password = data_set['password']
        expected_url_part = data_set['expected_url_part']
        
        print(f"--- Running Positive Test: {username} ---")
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_loginbtn()
        #Verifikasi dengan assert
        self.assertIn(expected_url_part, self.driver.current_url,
                    f"Failed: Successfully login, but cannot move to the URL: {expected_url_part}")
        print("Success!!")

    # 2. --- NEGATIVE CASE FUNCTION ---
    @data(*load_testdata('negative_cases'))#<--- CALL Helper Function

    def test_02_negative_login(self, data_set):
        """LGN-02,03,04: Verify error message when logging in with locked_out_user, 
        invalid username/password 
        and empty field checking
        """
        #Get the value, since data entry as a single dictionary
        username = data_set['username']
        password = data_set['password']
        expected_error = data_set['expected_error']

        print(f"--- Running Negative Test: {username} ---")
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_loginbtn()
        #Verifikasi dengan assert
        error_text = self.login_page.get_error_message()
        self.assertIn(expected_error, error_text,
                    f"Failed: Incorrect Error Message. Expectation: {expected_error}")
        print("Success!!")

    def test_03_failed_login_empty(self):
        """LGN-05: Verify error message when logging in with locked_out_user and invalid username/password """
        self.login_page.click_loginbtn()
        error_text = self.login_page.get_error_message()

        expected_msg = "Epic sadface: Username is required"
        self.assertEqual(error_text, expected_msg, f"Failed: Incorrect Error Message. Got {error_text}")

# --- (AUTO RUNNER) ---
if __name__ == "__main__":

    # pytest options
    pytest_args = [
        __file__,                                  # running this file
        "--html=Report_Test/Report_Login.html", # HTML Report to this folder
        "--self-contained-html",                   
        "-v"                                       
    ]

    print("Running...")
    pytest.main(pytest_args)
    