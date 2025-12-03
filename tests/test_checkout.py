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
            self.user_data = data_json['checkout_data']
    
    # Helper method to add two items and go to checkout page
    def add_two_items_and_go_to_checkout(self):
        self.inventory_page.add_item_by_index(0)
        self.inventory_page.add_item_by_index(1)
        self.inventory_page.click_cart_icon()
        self.cart_page.click_checkout()

    def test_01_02_access_checkout_info(self):
        """CASE 1 & 2: User add items and access checkout information page"""
        self.add_two_items_and_go_to_checkout()

        #Validate URL & Title
        self.assertIn("checkout-step-one.html", self.driver.current_url)
        title = self.checkout_page.get_page_title()
        self.assertEqual(title, "Checkout: Your Information", "FAILED: Incorrect Checkout Information Page Title")

    def test_03_validate_ui_components(self):
        """CASE 3: Validate UI Fields (Name, Zip/Postal Code, Buttons) are visible"""
        self.add_two_items_and_go_to_checkout()
        
        #Validate Fields Visible
        is_fields_visible = self.checkout_page.verify_fields_visible()
        self.assertTrue(is_fields_visible, "FAILED: One or more fields/buttons are not visible on Checkout Information Page")

    def test_04_fill_information_success(self):
        """CASE 4: Fill Information Successfully"""
        self.add_two_items_and_go_to_checkout()
        
        self.checkout_page.fill_information(
            self.user_data[0]['firstname'],
            self.user_data[0]['lastname'],
            self.user_data[0]['postalcode']
        )
    
    def test_05_negative_empty_firstname(self):
        """CASE 5: [NEGATIVE] Empty first name"""
        self.add_two_items_and_go_to_checkout()
        self.checkout_page.fill_information(None, "John", "123456")
        self.checkout_page.click_continue()
        self.assertEqual(self.checkout_page.get_error_message(), "Error: First Name is required")
    
    def test_06_negative_empty_lastname(self):
        """"CASE 6: [NEGATIVE] Empty last name"""
        self.add_two_items_and_go_to_checkout()
        self.checkout_page.fill_information("Tester", None, "123456")
        self.checkout_page.click_continue()
        self.assertEqual(self.checkout_page.get_error_message(), "Error: Last Name is required")
    
    def test_07_negative_empty_postalcode(self):
        """CASE 7: [NEGATIVE] Empty postal code"""
        self.add_two_items_and_go_to_checkout()
        self.checkout_page.fill_information("Tester", "John", None)
        self.checkout_page.click_continue()
        self.assertEqual(self.checkout_page.get_error_message(), "Error: Postal Code is required")
    
    def test_08_negative_all_empty(self):
        """CASE 8: [NEGATIVE] All fields empty (Priority Check)"""
        self.add_two_items_and_go_to_checkout()
        self.checkout_page.fill_information(None, None, None)
        self.checkout_page.click_continue()
        self.assertEqual(self.checkout_page.get_error_message(), "Error: First Name is required")

    def test_09_cancel_button_step_one(self):
        """CASE 9: Validate cancel button redirects to cart"""
        self.add_two_items_and_go_to_checkout()
        self.checkout_page.click_cancel()
        self.assertIn("cart.html", self.driver.current_url)
    
    def test_10_continue_to_overview(self):
        """CASE 10: Validate continue button redirects to Overview Page"""
        self.add_two_items_and_go_to_checkout()
        self.checkout_page.fill_information(
            self.user_data[0]['firstname'],
            self.user_data[0]['lastname'],
            self.user_data[0]['postalcode']
        )
        self.checkout_page.click_continue()

        self.assertIn("checkout-step-two.html", self.driver.current_url)
        title = self.checkout_page.get_page_title()
        self.assertEqual(title, "Checkout: Overview", "FAILED: Incorrect Checkout Overview Page Title")
    
    def test_11_validate_overview_calculations(self):
        """CASE 11: Validate logic calculation (Item Total + Tax = Total)"""
        self.test_10_continue_to_overview() #Go to overview page

        #price_list: mengambil harga satuan item. contoh: [29.99, 9.99]
        price_list = self.checkout_page.get_item_prices_as_float()
        #summary_values: Mengambil value di footer (Subtotal, Tax, Total)
        summary_values = self.checkout_page.get_summary_values()
        errors = []

        #Validate Subtotal
        #sum(price_list) -> sum automatically [29.99 + 9.99] = 39.98
        #after that compared to summary_values['subtotal'] on the screen
        if sum(price_list) != summary_values['subtotal']:
            errors.append(f"FAILED: Subtotal mismatch! Expected {sum(price_list)}, != label {summary_values['subtotal']}")
        
        #Validate Tax
        #self.user_data['tax_value'] -> get from JSON (3.20)
        #summary_values['tax'] -> get from screen
        if self.user_data[0]['tax_value'] != summary_values['tax']:
            errors.append(f"FAILED: Tax mismatch! Expected {self.user_data['tax_value']}, != Actual {summary_values['tax']}")
        
        #Validate Total
        #Calculated Total = Subtotal(from screen) + Tax(from screen)
        calculated_total = summary_values['subtotal'] + summary_values['tax']

        #Round means pembulatan decimal sehingga 2 angka dibelakang koma
        if round(calculated_total, 2) != round(summary_values['total'], 2):
            errors.append(f"FAILED: Total mismatch! Expected {calculated_total}, != Label {summary_values['total']}")
        
        if errors:
            self.fail(f"FAILED: {len(errors)} calculation errors found: {errors}")

    def test_12_cancel_button_overview_bug(self):
        """CASE 12: Validate cancel on overview (Expect: Cart, Actual:Inventory -> KNOWN ISSUE)"""
        self.test_10_continue_to_overview() #Go to overview page
        self.checkout_page.click_cancel()

        if "inventory.html" in self.driver.current_url:
            self.fail("ISSUE FOUND: Cancel button redirected to Product Page (Inventory), expected Cart Page.")
        self.assertIn("cart.html", self.driver.current_url)
    
    def test_13_finish_order(self):
        """CASE 13: Validate Finish Oder, Completed page and valu on cart badge reset"""
        self.test_10_continue_to_overview() #Go to overview page
        self.checkout_page.click_finish()

        self.assertIn("checkout-complete.html", self.driver.current_url)
        title = self.checkout_page.get_page_title()
        self.assertEqual(title, "Checkout: Complete!", "FAILED: Incorrect Checkout Completed Page Title")

        message = self.checkout_page.get_completed_message()
        self.assertEqual(message, "Thank you for your order!", "FAILED: Incorrect Completed Message Text")

        message = self.checkout_page.click_back_home()
        self.assertIn("inventory.html", self.driver.current_url)
        self.assertEqual(self.inventory_page.get_cart_badge_value(), 0, "FAILED: Cart Badge is not reset to 0 after order completion")


# --- (AUTO RUNNER) ---
if __name__ == "__main__":

    # pytest options
    pytest_args = [
        __file__,                                  # running this file
        "--html=Report_Test/Report_checkout_page_flow.html", # HTML Report to this folder
        "--self-contained-html",                   
        "-v"                                       
    ]

    print("Running...")
    pytest.main(pytest_args)