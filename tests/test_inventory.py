import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pages.inventory_page import sauceDemoInventoryPage
from tests.base_test import BaseTestLoggedIn
import re #<< for checking HTML logic
import pytest

class TestSauceDemoInventory(BaseTestLoggedIn):
    def setUp(self):
        super().setUp()
        self.inventory_page = sauceDemoInventoryPage(self.driver)
        self.logger.info("--- Inventory Page Test Started ---")

    def test_1_inventory_display(self):
        """Case1: Ensure that product page is show as usual"""
        self.logger.info("1. Title Page Checking...")
    
        #Title Checking
        title = self.inventory_page.get_page_title()
        try: 
            self.assertEqual(title, "Products", "Incorrect Page Title")
            self.logger.info(f"SUCCESS: Page title verified: '{title}'")
        except AssertionError as e:
            self.logger.error(f"FAILED: Expected title 'Products', Got '{title}")
            raise e

        #Checking item count
        item_count = self.inventory_page.get_inventory_count()
        self.logger.info(f"INFO: Found {item_count} items on inventory page.")
        try:
            self.assertGreater(item_count, 0, "Error: Item List is null")
            self.logger.info("SUCCESS: Inventory items loaded successfully.")
        except AssertionError as e:
            self.logger.error("FAILED: No items found on inventory page.")
            raise e

    def test_2_add_item_by_name(self):
        """Case2: Add Specific items to cart"""
        self.logger.info("Scenario: Add Specific Items by Name")
        
        #list add items
        item_to_add = [ 
            "Sauce Labs Fleece Jacket",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt"
        ]

        #First ensure that cart is empty
        initial_cart_count = self.inventory_page.get_cart_badge_value()
        self.logger.info(f"Initial Cart Count: {initial_cart_count}")
        
        #Second looping to add 3 items
        self.logger.info(f"Adding {len(item_to_add)} items...")
        for item in item_to_add:
            self.logger.info(f"On process to add: {item}...")
            self.inventory_page.add_item_by_name(item)

        #Check value on the cart > must be increased
        # Logic: Final Amount must be = First Amount (0) + Number of item in list (3)
        expected_total = initial_cart_count + len (item_to_add)
        actual_total = self.inventory_page.get_cart_badge_value()

        self.logger.info(f"INFO: Total in cart: {actual_total}")

        try:
            self.assertEqual(actual_total,expected_total)
            self.logger.info(f"SUCCESS: Cart count match. Expected {expected_total}, Got {actual_total}")
        except AssertionError as e:
            self.logger.info(f"FAILED! Cart count mismatch. Expected {expected_total}, Got {actual_total}")
            raise e
        
    def test_3_add_item_by_index(self):
        """Case3: Adding the top 3 items (index 0,1,2) to cart"""
        self.logger.info("Scenario: Add Items by Index (Top 3 items)")
        
        #First ensure that cart is empty
        initial_cart_count = self.inventory_page.get_cart_badge_value()
        #Second we want to get the top of 3 items
        item_count_to_add = 3
        
        for i in range(item_count_to_add):
            self.logger.info(f"Adding item at index {i}...")
            self.inventory_page.add_item_by_index(i)
        
        #Assert dynamic
        expected_total = initial_cart_count + item_count_to_add
        actual_total = self.inventory_page.get_cart_badge_value()

        try:
            self.assertEqual(actual_total,expected_total)
            self.logger.info(f"SUCCESS: Total on cart: {actual_total}")
        except AssertionError as e:
            self.logger.info(f"FAILED! Expected {expected_total} items, Got {actual_total}")
            raise e
        
    def test_4_sort_products(self):
        """Case4: Ensure that sorting can be used"""
        self.logger.info("Scenario: Product Sorting Verification")
        
        sort_options = {
            "za": "Name (Z to A)",
            "lohi": "Price (low to high)",
            "hilo": "Price (high to low)",
            "az": "Name (A to Z)"
        }
        
        #Loop get value and expected text
        for value, expected_text in sort_options.items():
            self.logger.info(f"Sorting Test: {expected_text} ({value})...")
            
            #Action
            self.inventory_page.product_sorting(value)

            #Validation
            current_text = self.inventory_page.get_active_sort_option()

            try:
                self.assertEqual(current_text, expected_text)
                self.logger.info(f"SUCCESS: Dropdown shows '{current_text}'")
            except AssertionError as e:
                self.logger.info(f"FAILED! Sorting {value} not active. It shows: {current_text}")
                raise e

    def test_5_open_cart(self):
        """Case5: Verified when click cart icon, will redirect to cart page."""
        self.logger.info("Scenario: Open Cart Page")
        
        self.inventory_page.click_cart_icon()

        #Assert to validate the URL
        current_url = self.driver.current_url
        
        try:
            self.assertIn("cart.html", current_url)
            self.logger.info(f"SUCCESS: Redirected to Cart Page ({current_url})")
        except AssertionError as e:
            self.logger.error(f"FAILED: URL mismatch. Got {current_url}")
            raise e
    
    def test_6_sidebar_menu(self):
        """Case6: Verified sidebar menu can clicked and opened"""
        self.logger.info("Scenario: Open Sidebar Menu")
        
        try:
            self.inventory_page.click_sidebar_menu()
            self.logger.info("PASSED: Sidebar menu clicked without error.")
        except Exception as e:
            self.logger.error(f"FAILED: Could not click sidebar menu. Error: {e}")
            raise e


    def test_7_validate_item_content(self):
        """Case7: Verified image, descriptions (without HTML code leak), Title(without HTML code leak), and Price"""
        self.logger.info("Scenario: Validate Item Content (Soft Assertion for Bugs)")
        
        all_items = self.inventory_page.get_all_items_data()
        errors = [] #Error Buffer (Soft Assertion)

        # Regex patterns for capturing leaked HTML or code
        # 1. <.*?>          : Captures any HTML tag (e.g., <div>, <br>, <b>)
        # 2. function\(\)   : Captures the text “function()”
        # 3. \(\)           : Captures empty parentheses “()” that often appear in method code
        # 4. Test\.all      : Captures specific text “Test.allTheThings” (a known bug)
        bad_patterns = [r"<.*?>", r"function\(\)", r"Test\.all"]
        self.logger.info(f"Scanning {len(all_items)} items for UI/Data defects...")

        for index, item in enumerate(all_items):
            #1. validate images not broken
            if not self.inventory_page.check_image_loaded(item['image_element']):
                message = f"FAILED: Images broken for items '{item['name']}'"
                errors.append(message)
                self.logger.warning(message)
                
            #2. validate price must be show and had "$" symbols
            if "$" not in item['prices']:
                message = f"FAILED: Incorrect Price Format on the '{item['name']}': {item['prices']}"
                errors.append(message)
                self.logger.warning(message)
                
            #3 and 4. Validate the content (Title and Descriptions)
            #Looping pattern for checking two fields in one run
            for pattern in bad_patterns:
                #Description Checking
                if re.search(pattern, item['descriptions']):
                    message = f"BUG FOUND: HTML/Code show in descriptions '{item['name']}', {item['descriptions']}"
                    errors.append(message)
                    self.logger.error(message)
                    
                #Title Checking
                if re.search(pattern, item['name']):
                    message = f"BUG FOUND: HTML/Code show in descriptions '{item['name']}'"
                    errors.append(message)
                    self.logger.error(message)
                    
        #FINAL ASSERTIONS
        if errors:
            self.logger.info("=====================================")
            self.logger.error(f"TEST FAILED: Found {len(errors)} UI/Data Issues!")
            self.logger.info("=====================================")
            self.fail(f"FAILED TEST! {len(errors)} issues found. Check logs for details.")
        else:
            self.logger.info("PASSED: All product contents are valid.")


    def test_8_click_image(self):
        """Case8: Validate if user clicking image it will redirect to product/item details"""
        self.logger.info("Scenario: Click Item Title Navigation")
        self.inventory_page.click_item_image_by_index(0)
        
        try:
            self.assertIn("inventory-item.html", self.driver.current_url)
            self.logger.info("SUCCESS: Redirected to Product Details via Image.")
        except AssertionError as e:
            self.logger.error("FAILED: Did not redirected to details page.")
            raise e

    def test_9_click_title(self):
        """Case9: Validate if user clicking title it will redirect to product/item details"""
        self.logger.info("Scenario: Click Item Title Navigation")
        
        self.inventory_page.click_item_title_by_index(0)
        
        try:
            self.assertIn("inventory-item.html", self.driver.current_url)
            self.logger.info("PASSED: Redirected to Product Details via Title.")
        except AssertionError as e:
            self.logger.error("FAILED: Did not redirect to details page.")
            raise e
        
    def test_10_logout(self):
        """"Case10: Test Logout Functionality"""
        self.logger.info("Scenario: Logout Flow")
        
        self.inventory_page.click_sidebar_menu()
        self.inventory_page.click_logout()
        
        current_url = self.driver.current_url
        try:
            self.assertNotIn("inventory.html", current_url)
            # Validate login button is show
            self.driver.find_element(*self.login_page.LOGIN_BUTTON).is_displayed()
            self.logger.info("PASSED: Successfully logged out and Login button is visible.")
        except AssertionError as e:
            self.logger.error("FAILED: Still in inventory page or Login button not found.")
            raise e
        except Exception as e:
            self.logger.error(f"FAILED: Error during validation: {e}")
            raise e

# --- (AUTO RUNNER) ---
if __name__ == "__main__":

    # pytest options
    pytest_args = [
        __file__,                                  # running this file
        "--html=Report_Test/Report_List_Product.html", # HTML Report to this folder
        "--self-contained-html",                   
        "-v"                                       
    ]
    pytest.main(pytest_args)