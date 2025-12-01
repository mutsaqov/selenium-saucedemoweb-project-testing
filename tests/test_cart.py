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
        
    def test_01_access_cart_page(self):
        """CASE 1: Validate user successfully access cart page"""
        self.inventory_page.click_cart_icon()
        title = self.cart_page.get_page_title()
        self.assertEqual(title, "Your Cart", "FAILED: Incorrect Page Title")
        
    def test_02_03_empty_cart_dispkay(self):
        """CASE 2 AND 3: VALIDATE EMPTY CART DISPLAY & BUTTONS"""
        
        #Access Cart without items add
        self.inventory_page.click_cart_icon()
        
        #Validate items is empty
        items = self.cart_page.get_all_cart_item()
        self.assertEqual(len(items), 0, "FAILED: Cart is not empty")
        
        #Validate the buttons is show
        print("Checking Buttons Visibility....")
        self.assertTrue(self.driver.find_element(*self.cart_page.BTN_CONTINUE_SHOPPING).is_displayed(), "FAILED: Continue Shopping Button is not visible")
        self.assertTrue(self.driver.find_element(*self.cart_page.BTN_CHECKOUT).is_displayed(), "FAILED: Checkout Button is not visible")
    
    
    def test_04_validate_added_items(self):
        """Case 4: Validate cart shows added items (2 items sample)"""
        
        # Pre-condition: Add 2 items
        print("Adding 2 items from inventory...")
        self.inventory_page.add_item_by_index(0) 
        self.inventory_page.add_item_by_index(1) 
        
        self.inventory_page.click_cart_icon()
        
        items = self.cart_page.get_all_cart_item()
        self.assertEqual(len(items), 2, "FAILED: Cart is empty")
        
    def test_05_06_validate_item_details(self):
        """Case 5 & 6: Validate QTY, Price, Title, Description (DYNAMIC DATA LOGIC)"""
        
        #STEP 1: GET ITEM NAME DYNAMICALLY
        #Get first item (index 0) that show in the screen
        #whatever the item is, script will get the name
        target_index = 0
        expected_item_name = self.inventory_page.get_item_name_by_index(target_index)
        
        print(f"INFO: System selected item dynamically: {expected_item_name}")
        
        #STEP 2: ADD ITEM TO CART BY NAME
        self.inventory_page.add_item_by_name(expected_item_name)
        
        #STEP 3: GO TO CART
        self.inventory_page.click_cart_icon()
        
        #STEP 4: Validate
        #Get first item data in cart
        cart_data = self.cart_page.get_item_data_by_index(0)
        print(f"INFO: Data found in cart: {cart_data}")
        
        #Assertions
        self.assertEqual(cart_data['quantity'], '1', "FAILED: Quantity mismatch")
        
        #Validate the name of item: Compare cart vs name that we get from inventory
        self.assertEqual(cart_data['name'], expected_item_name, "FAILED: Item name mismatch")
        
        self.assertTrue("$" in cart_data['price'], "FAILED: Incorrect price format")
        self.assertTrue(len(cart_data['description']) > 0, "FAILED: Description is empty")
    
    def test_07_remove_item(self):
        """Case 7: Validate Remove button functionality"""
        
        #Adding 1 item
        self.inventory_page.add_item_by_index(0)
        initial_badge = self.inventory_page.get_cart_badge_value()
        self.inventory_page.click_cart_icon()
        
        #Remove action
        print("Removing item...")
        self.cart_page.click_remove_item_by_index(0)
        
        #Validation 1 : empty list
        items = self.cart_page.get_all_cart_item()
        self.assertEqual(len(items), 0, "FAILED: Item is not removed")
        
        #Validation 2 : badge count
        final_badge = self.inventory_page.get_cart_badge_value()
        self.assertEqual(final_badge, initial_badge - 1, "FAILED: Badge count mismatch")
        
    def test_08_continue_shopping(self):
        """Case 8: Validate Continue Shopping button functionality"""
        self.inventory_page.click_cart_icon()
        self.cart_page.click_continue_shopping()
        
        #Validate the redirection
        self.assertIn("inventory.html", self.driver.current_url, "FAILED: Not redirected to inventory page")
        self.assertEqual(self.inventory_page.get_page_title(), "Products")
    
    def test_09_checkout_navigation(self):
        """Case 9: Validate Checkout button functionality"""
        
        #First add item to cart
        #self.inventory_page.add_item_by_index(1)
        #self.inventory_page.add_item_by_index(2)
        for i in range(2):
            self.inventory_page.add_item_by_index(i)
        self.inventory_page.click_cart_icon()
        
        self.cart_page.click_checkout()
        
        #Validate the redirection 
        self.assertIn("checkout-step-one.html", self.driver.current_url, "FAILED: Not redirected to checkout page")
        
    def test_10_negative_remove_all_item(self):
        """Case 10: [NEGATIVE CASE] Remove all items and ensure list empty"""
        
        #add 3 items
        for i in range(3):
            self.inventory_page.add_item_by_index(i)
        
        self.inventory_page.click_cart_icon()
        
        #Deleted 1 by 1 until cart is empty
        while len(self.cart_page.get_all_cart_item()) > 0:
            self.cart_page.click_remove_item_by_index(0)
            time.sleep(0.5)
        
        items_left = self.cart_page.get_all_cart_item()
        self.assertEqual(len(items_left), 0, "FAILED: Cart not fully empty")
    
    def test_11_negative_checkout_empty_cart(self):
        """CASE 11: [NEGATIVE CASE] Checkout button should be disabled if cart is empty"""
        self.inventory_page.click_cart_icon()
        
        #Check is the button enabled?
        is_enabled = self.cart_page.is_checkout_enabled()
        
        if is_enabled:
            self.cart_page.click_checkout()
            current_url = self.driver.current_url
            
            #If URL move to checkout page, we found bug here
            if"checkout-step-one.html" in current_url:
                print("\n ===== BUG REPORT =====")
                print("Description: User can proceed to checkout with empty cart")
                
                #make test failed so it can be write on report
                self.fail("BUG FOUND: Checkout button is enabled and functional on empty cart! ")
        
        print("SUCCESS: Checkout button is correctly disabled!")
        

# --- (AUTO RUNNER) ---
if __name__ == "__main__":

    # pytest options
    pytest_args = [
        __file__,                                  # running this file
        "--html=Report_Test/Report_cart_page.html", # HTML Report to this folder
        "--self-contained-html",                   
        "-v"                                       
    ]

    print("Running...")
    pytest.main(pytest_args)