import unittest
import sys
import os
import time
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from pages.cart_page import sauceDemoCartPage
from pages.inventory_page import sauceDemoInventoryPage
from tests.base_test import BaseTestLoggedIn

class TestSauceDemoCart(BaseTestLoggedIn):
    
    def setUp(self):
        super().setUp()
        self.inventory_page = sauceDemoInventoryPage(self.driver)
        self.cart_page = sauceDemoCartPage(self.driver)
        
        self.logger.info("--- Cart Page Test Started ---")
        
    def test_01_access_cart_page(self):
        """CASE 1: Validate user successfully access cart page"""
        self.logger.info("Scenario: Access Cart Page")
        
        self.inventory_page.click_cart_icon()
        title = self.cart_page.get_page_title()
        
        try:
            self.assertEqual(title, "Your Cart")
            self.logger.info("PASSED: Correct Page Title 'Your Cart'")
        except AssertionError as e:
            self.logger.error(f"FAILED: Incorrect Page Title. Got '{title}'")
            raise e
        
    def test_02_03_empty_cart_dispkay(self):
        """CASE 2 AND 3: VALIDATE EMPTY CART DISPLAY & BUTTONS"""
        self.logger.info("Scenario: Empty Cart Display & Buttons Visibility")
        
        #Access Cart without items add
        self.inventory_page.click_cart_icon()
        
        #Validate items is empty
        items = self.cart_page.get_all_cart_item()
        try:
            self.assertEqual(len(items), 0)
            self.logger.info("PASSED: Cart is empty as expected.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Cart is NOT empty. Found {len(items)} items.")
            raise e
        
        #Validate the buttons is show
        self.logger.info("Checking Buttons Visibility...")
        try:
            continue_btn = self.driver.find_element(*self.cart_page.BTN_CONTINUE_SHOPPING).is_displayed()
            checkout_btn = self.driver.find_element(*self.cart_page.BTN_CHECKOUT).is_displayed()
            
            if continue_btn and checkout_btn:
                self.logger.info("PASSED: 'Continue Shopping' and 'Checkout' buttons are visible.")
            else:
                self.logger.error("FAILED: One or more buttons are missing.")
                self.fail("Buttons missing.")
        except Exception as e:
            self.logger.error(f"FAILED: Error finding buttons: {e}")
            raise e
    
    
    def test_04_validate_added_items(self):
        """Case 4: Validate cart shows added items (2 items sample)"""
        self.logger.info("Scenario: Validate Item Count in Cart")
        
        # Pre-condition: Add 2 items
        self.logger.info("Adding 2 items from inventory...")
        self.inventory_page.add_item_by_index(0) 
        self.inventory_page.add_item_by_index(1) 
        
        self.inventory_page.click_cart_icon()
        
        items = self.cart_page.get_all_cart_item()
        try:
            self.assertEqual(len(items), 2)
            self.logger.info("SUCCESS: Cart contains 2 items.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Cart item count mismatch. Expected 2, Got {len(items)}")
            raise e
        
    def test_05_06_validate_item_details(self):
        """Case 5 & 6: Validate QTY, Price, Title, Description (DYNAMIC DATA LOGIC)"""
        self.logger.info("Scenario: Validate Item Details (Dynamic Data Match)")
        
        #STEP 1: GET ITEM NAME DYNAMICALLY
        #Get first item (index 0) that show in the screen
        #whatever the item is, script will get the name
        target_index = 0
        expected_item_name = self.inventory_page.get_item_name_by_index(target_index)
        
        self.logger.info(f"INFO: System selected item dynamically: {expected_item_name}")
        
        #STEP 2: ADD ITEM TO CART BY NAME
        self.inventory_page.add_item_by_name(expected_item_name)
        
        #STEP 3: GO TO CART
        self.inventory_page.click_cart_icon()
        
        #STEP 4: Validate
        #Get first item data in cart
        cart_data = self.cart_page.get_item_data_by_index(0)
        self.logger.info(f"INFO: Data found in cart: {cart_data}")
        
        #Assertions
        try: 
            #Check Quantity
            self.assertEqual(cart_data['quantity'], '1')
            #Check the name of item: Compare cart vs name that we get from inventory
            self.assertEqual(cart_data['name'], expected_item_name)
            #Check Price format
            self.assertTrue("$" in cart_data['price'])
            #Check Description Not Empty
            self.assertTrue(len(cart_data['description']) > 0)
            
            self.logger.info("SUCCESS: All item details (Qty, Name, Price, Description) match inventory data.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Data Mismatch! \nExpected Name: {expected_item_name} \nActual Data: {cart_data}")
            raise e
    
    def test_07_remove_item(self):
        """Case 7: Validate Remove button functionality"""
        self.logger.info("Scenario: Remove Item from Cart")
        
        #Adding 1 item
        self.inventory_page.add_item_by_index(0)
        initial_badge = self.inventory_page.get_cart_badge_value()
        self.inventory_page.click_cart_icon()
        
        #Remove action
        self.logger.info("Removing item...")
        self.cart_page.click_remove_item_by_index(0)
        
        #Validation 1 : empty list
        items = self.cart_page.get_all_cart_item()
        try:
            self.assertEqual(len(items), 0)
            self.logger.info("PASSED: Item removed from list.")
        except AssertionError as e:
            self.logger.error("FAILED: Item still exists in cart list.")
            raise e
        
        #Validation 2 : badge count
        final_badge = self.inventory_page.get_cart_badge_value()
        try:
            self.assertEqual(final_badge, initial_badge - 1)
            self.logger.info(f"PASSED: Badge updated from {initial_badge} to {final_badge}.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Badge mismatch. Got {final_badge}")
            raise e
        
    def test_08_continue_shopping(self):
        """Case 8: Validate Continue Shopping button functionality"""
        self.logger.info("Scenario: Continue Shopping Navigation")
        
        self.inventory_page.click_cart_icon()
        self.cart_page.click_continue_shopping()
        
        #Validate the redirection
        current_url = self.driver.current_url
        try:
            self.assertIn("inventory.html", current_url)
            self.assertEqual(self.inventory_page.get_page_title(), "Products")
            self.logger.info("SUCCESS: Redirected back to Inventory Page.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Incorrect Redirection. URL: {current_url}")
            raise e
    
    def test_09_checkout_navigation(self):
        """Case 9: Validate Checkout button functionality"""
        self.logger.info("Scenario: Checkout Navigation")
        
        #First add item to cart
        #self.inventory_page.add_item_by_index(1)
        #self.inventory_page.add_item_by_index(2)
        for i in range(2):
            self.inventory_page.add_item_by_index(i)
        self.inventory_page.click_cart_icon()
        
        self.cart_page.click_checkout()
        
        #Validate the redirection 
        try:
            self.assertIn("checkout-step-one.html", self.driver.current_url)
            self.logger.info("PASSED: Successfully entered Checkout Step One.")
        except AssertionError as e:
            self.logger.error("FAILED: Did not redirect to checkout page.")
            raise e
        
    def test_10_negative_remove_all_item(self):
        """Case 10: [NEGATIVE CASE] Remove all items and ensure list empty"""
        
        self.logger.info("Scenario: Remove All Items Loop")
        
        #add 3 items
        for i in range(3):
            self.inventory_page.add_item_by_index(i)
        
        self.inventory_page.click_cart_icon()
        
        #Deleted 1 by 1 until cart is empty
        while len(self.cart_page.get_all_cart_item()) > 0:
            self.cart_page.click_remove_item_by_index(0)
            time.sleep(0.5)
        
        items_left = self.cart_page.get_all_cart_item()
        try:
            self.assertEqual(len(items_left), 0)
            self.logger.info("PASSED: All items removed successfully.")
        except AssertionError as e:
            self.logger.error("FAILED: Cart is not fully empty.")
            raise e
    
    def test_11_negative_checkout_empty_cart(self):
        """CASE 11: [NEGATIVE CASE] Checkout button should be disabled if cart is empty"""
        
        self.logger.info("Scenario: Validate Checkout on Empty Cart")
        self.inventory_page.click_cart_icon()
        
        #Check is the button enabled?
        self.logger.info("Checking if Checkout button is enabled...")
        is_enabled = self.cart_page.is_checkout_enabled()
        
        if is_enabled:
            self.logger.warning("ALERT: Checkout button is ENABLED (Should be disabled). Attempting to click...")
            
            # Try to click
            self.cart_page.click_checkout()
            current_url = self.driver.current_url
            
            # 3. VALIDATE
            if "checkout-step-one.html" in current_url:
                self.logger.error("BUG REPORT: User successfully navigated to checkout page with empty cart!")
                self.fail("BUG FOUND: Checkout button is enabled and functional on empty cart!")
            else:
                self.logger.info("PASSED: Button was enabled, but click did not redirect (Safe).")
        else:
            self.logger.info("PASSED: Checkout button is correctly disabled.")
        

# --- (AUTO RUNNER) ---
if __name__ == "__main__":

    # pytest options
    pytest_args = [
        __file__,                                  # running this file
        "--html=Report_Test/Report_cart_page.html", # HTML Report to this folder
        "--self-contained-html",                   
        "-v"                                       
    ]

    pytest.main(pytest_args)