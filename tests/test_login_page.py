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
        self.logger.info("Open SauceDemo web...")
        self.inventory_page = sauceDemoInventoryPage(self.driver)
        
    # 1. --- POSITIVE CASE FUNCTION ---
    @data(*load_testdata('positive_cases')) #<--- CALL Helper Function

    def test_01_positive_login(self, data_set):
        """LGN-01: Verify successful login with valid standard_user credentials. """
        #Get the value, since data entry as a single dictionary
        username = data_set['username']
        password = data_set['password']
        expected_url_part = data_set['expected_url_part']
        
        self.logger.info(f"--- Running Positive Test: {username} ---")
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_loginbtn()
        
        #Validation
        self.logger.info("Validation Redirection URL...")
        current_url = self.driver.current_url
        
        try:
            self.assertIn(expected_url_part, current_url)
            self.logger.info(f"SUCCESS: User successfully redirect to ' {current_url}'")
        except AssertionError as e:
            self.logger.error(f"FAILED: URL Mismatch. Expected '{expected_url_part}' in '{current_url}'")
            raise e
            
            
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

        self.logger.info(f"--- Running Negative Test: {username} ---")
        self.login_page.enter_username(username)
        self.login_page.enter_password(password)
        self.login_page.click_loginbtn()

        #Validation
        self.logger.info("Validating error messages...")
        actual_error = self.login_page.get_error_message()
        
        try:
            self.assertIn(expected_error, actual_error)
            self.logger.info(f"SUCCESS: Error message matches expectations: '{actual_error}'")
        except AssertionError as e:
            self.logger.error(f"FAILED: Error message mismatch. Expected '{expected_error}', Got '{actual_error}'")
            raise e
            
    def test_03_failed_login_empty(self):
        """LGN-05: Verify error message when logging in whithout username/password """
        self.logger.info("Scenario: Login with Empty Username & Password")
        self.login_page.click_loginbtn()
        actual_error_text = self.login_page.get_error_message()
        expected_msg = "Epic sadface: Username is required"
        
        try:
            self.assertEqual(actual_error_text, expected_msg)
            self.logger.info("SUCCESS: Correct error message for empty fields displayed.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Expected '{expected_msg}', Got '{actual_error_text}'")
            raise e

# --- (AUTO RUNNER) ---
if __name__ == "__main__":

    # pytest options
    pytest_args = [
        __file__,                                  # running this file
        "--html=Report_Test/Report_Login.html", # HTML Report to this folder
        "--self-contained-html",                   
        "-v"                                       
    ]
    pytest.main(pytest_args)
    