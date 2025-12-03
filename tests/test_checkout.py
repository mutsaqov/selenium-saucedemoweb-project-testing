import unittest
import sys
import os
import json
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from pages.inventory_page import sauceDemoInventoryPage
from pages.cart_page import sauceDemoCartPage
from pages.checkout_page import sauceDemoCheckoutPage
from tests.base_test import BaseTestLoggedIn

class TestSauceDemoCheckout(BaseTestLoggedIn):

    def setUp(self):
        super().setUp()
        #Load user data from JSON
        self.inventory_page = sauceDemoInventoryPage(self.driver)
        self.cart_page = sauceDemoCartPage(self.driver)
        self.checkout_page = sauceDemoCheckoutPage(self.driver)

        current_dir = os.path.dirname(__file__)
        data_file_path = os.path.join(current_dir, "..", "data", "users.json")
        with open(data_file_path, 'r') as f:
            data_json = json.load(f)
            self.user_data = data_json['checkout_data'][0]
            
        self.logger.info("--- Checkout Page Test Started ---")
    
    # Helper method to add two items and go to checkout page
    def add_two_items_and_go_to_checkout(self):
        """Helper function to setup precondition"""
        self.logger.info("Precondition: Adding 2 items and navigating to checkout...")
        self.inventory_page.add_item_by_index(0)
        self.inventory_page.add_item_by_index(1)
        self.inventory_page.click_cart_icon()
        self.cart_page.click_checkout()

    def test_01_02_access_checkout_info(self):
        """CASE 1 & 2: User add items and access checkout information page"""
        self.logger.info("Scenario: Access Checkout Step One (Information Page)")
        self.add_two_items_and_go_to_checkout()

        #Validate URL
        try:
            self.assertIn("checkout-step-one.html", self.driver.current_url)
            self.logger.info("PASSED: URL is correct.")
        except AssertionError as e:
            self.logger.error(f"FAILED: URL mismatch. Got {self.driver.current_url}")
            raise e
        
        #Validate Title
        title = self.checkout_page.get_page_title()
        try:
            self.assertEqual(title, "Checkout: Your Information")
            self.logger.info("PASSED: Page title verified.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Title mismatch. Got '{title}'")
            raise e

    def test_03_validate_ui_components(self):
        """CASE 3: Validate UI Fields (Name, Zip/Postal Code, Buttons) are visible"""
        self.logger.info("Scenario: Validate UI Components Visibility")
        self.add_two_items_and_go_to_checkout()
        
        #Validate Fields Visible
        try:
            is_visible = self.checkout_page.verify_fields_visible()
            self.assertTrue(is_visible)
            self.logger.info("PASSED: All input fields are visible.")
        except AssertionError as e:
            self.logger.error("FAILED: One or more input fields are missing.")
            raise e
        
    def test_04_fill_information_success(self):
        """CASE 4: Fill Information Successfully"""
        self.logger.info("Scenario: Fill Checkout Information (Positive)")
        self.add_two_items_and_go_to_checkout()
        
        self.logger.info(f"Inputting data: {self.user_data['firstname']} {self.user_data['lastname']}")
        self.checkout_page.fill_information(
            self.user_data['firstname'],
            self.user_data['lastname'],
            self.user_data['postalcode']
        )
        self.logger.info("PASSED: Data input successful (No errors raised).")
    
    def test_05_negative_empty_firstname(self):
        """CASE 5: [NEGATIVE] Empty first name"""
        self.logger.info("Scenario: Validate Error for Empty First Name")
        
        self.add_two_items_and_go_to_checkout()
        self.checkout_page.fill_information(None, "John", "123456")
        self.checkout_page.click_continue()
        
        message = self.checkout_page.get_error_message()
        try:
            self.assertEqual(message, "Error: First Name is required")
            self.logger.info("PASSED: Correct error message displayed.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Error message mismatch. Got '{message}'")
            raise e
    
    def test_06_negative_empty_lastname(self):
        """"CASE 6: [NEGATIVE] Empty last name"""
        self.logger.info("Scenario: Validate Error for Empty Last Name")
        
        self.add_two_items_and_go_to_checkout()
        self.checkout_page.fill_information("Tester", None, "123456")
        self.checkout_page.click_continue()
        
        message = self.checkout_page.get_error_message()
        try:
            self.assertEqual(message, "Error: Last Name is required")
            self.logger.info("PASSED: Correct error message displayed.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Error message mismatch. Got '{message}'")
            raise e
    
    def test_07_negative_empty_postalcode(self):
        """CASE 7: [NEGATIVE] Empty postal code"""
        self.logger.info("Scenario: Validate Error for Empty Zip Code")
        self.add_two_items_and_go_to_checkout()
        
        self.checkout_page.fill_information("Tester", "John", None)
        self.checkout_page.click_continue()
        
        message = self.checkout_page.get_error_message()
        try:
            self.assertEqual(message, "Error: Postal Code is required")
            self.logger.info("PASSED: Correct error message displayed.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Error message mismatch. Got '{message}'")
            raise e
    
    def test_08_negative_all_empty(self):
        """CASE 8: [NEGATIVE] All fields empty (Priority Check)"""
        self.logger.info("Scenario: Validate Priority Error (All Empty)")
        self.add_two_items_and_go_to_checkout()
        self.checkout_page.fill_information(None, None, None)
        self.checkout_page.click_continue()
        
        message = self.checkout_page.get_error_message()
        try:
            self.assertEqual(message, "Error: First Name is required")
            self.logger.info("PASSED: System correctly prioritizes First Name error.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Priority logic wrong. Got '{message}'")
            raise e

    def test_09_cancel_button_step_one(self):
        """CASE 9: Validate cancel button redirects to cart"""
        self.logger.info("Scenario: Cancel Button Navigation (Step One)")
        self.add_two_items_and_go_to_checkout()
        self.checkout_page.click_cancel()
        
        try:
            self.assertIn("cart.html", self.driver.current_url)
            self.logger.info("PASSED: Redirected back to Cart.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Navigation error. Current URL: {self.driver.current_url}")
            raise e
    
    def test_10_continue_to_overview(self):
        """CASE 10: Validate continue button redirects to Overview Page"""
        self.logger.info("Scenario: Continue to Overview Page")
        self.add_two_items_and_go_to_checkout()
        self.checkout_page.fill_information(
            self.user_data['firstname'],
            self.user_data['lastname'],
            self.user_data['postalcode']
        )
        self.checkout_page.click_continue()

        # Validate URL & Title
        try:
            self.assertIn("checkout-step-two.html", self.driver.current_url)
            title = self.checkout_page.get_page_title()
            self.assertEqual(title, "Checkout: Overview")
            self.logger.info("PASSED: Successfully entered Overview Page.")
        except AssertionError as e:
            self.logger.error("FAILED: Did not enter Overview page correctly.")
            raise e
    
    def test_11_validate_overview_calculations(self):
        """CASE 11: Validate logic calculation (Item Total + Tax = Total)"""
        self.logger.info("Scenario: Validate Math Calculations (Subtotal, Tax, Total)")
        
        self.test_10_continue_to_overview() #Go to overview page
    
        #price_list: mengambil harga satuan item. contoh: [29.99, 9.99]
        price_list = self.checkout_page.get_item_prices_as_float()
        #summary_values: Mengambil value di footer (Subtotal, Tax, Total)
        summary_values = self.checkout_page.get_summary_values()
        self.logger.info(f"Prices Found: {price_list}")
        self.logger.info(f"Summary Labels: {summary_values}")
        
        errors = []

        #Validate Subtotal
        #sum(price_list) -> sum automatically [29.99 + 9.99] = 39.98
        #after that compared to summary_values['subtotal'] on the screen
        if sum(price_list) != summary_values['subtotal']:
            message = f"FAILED: Subtotal mismatch! Expected {sum(price_list)}, != label {summary_values['subtotal']}"
            errors.append(message)
            self.logger.error(message)
        
        #Validate Tax
        #self.user_data['tax_value'] -> get from JSON (3.20)
        #summary_values['tax'] -> get from screen
        if self.user_data['tax_value'] != summary_values['tax']:
            message = f"FAILED: Tax mismatch! Expected {self.user_data['tax_value']}, != Actual {summary_values['tax']}"
            errors.append(message)
            self.logger.error(message)

        
        #Validate Total
        #Calculated Total = Subtotal(from screen) + Tax(from screen)
        calculated_total = summary_values['subtotal'] + summary_values['tax']

        #Round means pembulatan decimal sehingga 2 angka dibelakang koma
        if round(calculated_total, 2) != round(summary_values['total'], 2):
            message = f"FAILED: Total mismatch! Expected {calculated_total}, != Label {summary_values['total']}"
            errors.append(message)
            self.logger.error(message)
        
        if errors:
            self.fail(f"FAILED: {len(errors)} calculation errors found: {errors}")
        else:
            self.logger.info("PASSED: All calculations are correct.")

    def test_12_cancel_button_overview_bug(self):
        """CASE 12: Validate cancel on overview (Expect: Cart, Actual:Inventory -> KNOWN ISSUE)"""
        self.logger.info("Scenario: Cancel Button Navigation (Overview) - BUG CHECK")
        
        self.test_10_continue_to_overview() #Go to overview page
        
        self.logger.info("Clicking Cancel Button...")
        self.checkout_page.click_cancel()

        if "inventory.html" in self.driver.current_url:
            self.logger.error("BUG CONFIRMED: Cancel button redirected to Inventory Page instead of Cart.")
            self.fail("ISSUE FOUND: Cancel button redirected to Product Page (Inventory), expected Cart Page.")
        elif "cart.html" in self.driver.current_url:
            self.logger.info("PASSED: Redirected correctly to Cart Page (Bug fixed?).")
        else:
            self.logger.warning(f"Unexpected redirection to: {self.driver.current_url}")
    
    def test_13_finish_order(self):
        """CASE 13: Validate Finish Oder, Completed page and valu on cart badge reset"""
        self.logger.info("Scenario: Finish Order & Badge Reset")
        
        self.test_10_continue_to_overview() #Go to overview page
        
        self.logger.info("Clicking Finish Button...")
        self.checkout_page.click_finish()

        # 1. Validate Complete Page
        try:
            self.assertIn("checkout-complete.html", self.driver.current_url)
            self.assertEqual(self.checkout_page.get_page_title(), "Checkout: Complete!")
            
            message = self.checkout_page.get_completed_message()
            self.assertEqual(message, "Thank you for your order!")
            self.logger.info("PASSED: Order Completed successfully.")
        except AssertionError as e:
            self.logger.error("FAILED: Order completion page mismatch.")
            raise e

        # 2. Validate Back Home & Badge
        self.logger.info("Clicking Back Home...")
        self.checkout_page.click_back_home()
        
        try:
            self.assertIn("inventory.html", self.driver.current_url)
            badge = self.inventory_page.get_cart_badge_value()
            self.assertEqual(badge, 0)
            self.logger.info("PASSED: Redirected to Inventory and Cart Badge is 0.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Badge or Redirection mismatch. Badge: {badge}")
            raise e


# --- (AUTO RUNNER) ---
if __name__ == "__main__":

    # pytest options
    pytest_args = [
        __file__,                                  # running this file
        "--html=Report_Test/Report_checkout_page_flow.html", # HTML Report to this folder
        "--self-contained-html",                   
        "-v"                                       
    ]
    pytest.main(pytest_args)