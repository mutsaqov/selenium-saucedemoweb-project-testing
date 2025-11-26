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

    def test_1_inventory_display(self):
        """Case1: Ensure that product page is show as usual"""
        print("1. Title Page Checking...")
        title = self.inventory_page.get_page_title()
        self.assertEqual(title, "Products", "Incorrect Page Title")

        print("2. Total Item on the list checking...")
        item_count = self.inventory_page.get_inventory_count()
        print(f"INFO: Found {item_count} items on inventory page.")
        #Add assert to check test is success while the page is not null 
        self.assertGreater(item_count, 0, "Error: Item List is null")

    def test_2_add_item_by_name(self):
        """Case2: Add Specific items to cart"""
        #list add items
        item_to_add = [ 
            "Sauce Labs Fleece Jacket",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt"
        ]

        #First ensure that cart is empty
        initial_cart_count = self.inventory_page.get_cart_badge_value()

        #Second looping to add 3 items
        print(f"Adding {len(item_to_add)} items...")
        for item in item_to_add:
            print(f"On process to add: {item}...")
            self.inventory_page.add_item_by_name(item)

        #Check value on the cart > must be increased
        # Logic: Final Amount must be = First Amount (0) + Number of item in list (3)
        expected_total = initial_cart_count + len (item_to_add)
        actual_total = self.inventory_page.get_cart_badge_value()

        print(f"INFO: Total in cart: {actual_total}")

        self.assertEqual(
            actual_total,
            expected_total,
            f"FAILED! It should be {expected_total} items, but only {actual_total}"
        )

    def test_3_add_item_by_index(self):
        """Case3: Adding the top 3 items (index 0,1,2) to cart"""
        
        #First ensure that cart is empty
        initial_cart_count = self.inventory_page.get_cart_badge_value()

        #Second we want to get the top of 3 items
        item_count_to_add = 3
        print(f"On Process to add: {item_count_to_add} items by Index")
        
        for i in range(item_count_to_add):
            print(f"Adding item at index {i}...")
            self.inventory_page.add_item_by_index(i)
        
        #Assert dynamic
        expected_total = initial_cart_count + item_count_to_add
        actual_total = self.inventory_page.get_cart_badge_value()

        print(f"INFO: Total on cart: {actual_total}")
        self.assertEqual(
            actual_total,
            expected_total,
            f"FAILED! It should be {expected_total} items, but only {actual_total}"
        )

    def test_4_sort_products(self):
        """Case4: Ensure that sorting can be used"""
        sort_options = {
            "za": "Name (Z to A)",
            "lohi": "Price (low to high)",
            "hilo": "Price (high to low)",
            "az": "Name (A to Z)"
        }
        print(f"Start test {len(sort_options)} sorting options")

        #Loop get value and expected text
        for value, expected_text in sort_options.items():
            print(f"Sorting Test: {expected_text} ({value})...")
            
            #First, do sorting action
            self.inventory_page.product_sorting(value)

            #second, validate: Is the text in dropdown, successfully change?
            current_text = self.inventory_page.get_active_sort_option()

            self.assertEqual(
                current_text,
                expected_text,
                f"FAILED! Sorting {value} not active. It shows: {current_text}"
            )

    def test_5_open_cart(self):
        """Case5: Verified when click cart icon, will redirect to cart page."""
        print("Navigating to cart page....")
        self.inventory_page.click_cart_icon()

        #Assert to validate the URL
        current_url = self.driver.current_url
        self.assertIn("cart.html", current_url, "Failed!")
    
    def test_6_sidebar_menu(self):
        """Case6: Verified sidebar menu can clicked and opened"""
        print("Opening Sidebar menu....")
        self.inventory_page.click_sidebar_menu()
        pass


    def test_7_validate_item_content(self):
        """Case7: Verified image, descriptions (without HTML code leak), Title(without HTML code leak), and Price"""

        print("In progress checking all items...")
        all_items = self.inventory_page.get_all_items_data()
        errors = [] #Error Buffer (Soft Assertion)

        # Regex patterns for capturing leaked HTML or code
        # 1. <.*?>          : Captures any HTML tag (e.g., <div>, <br>, <b>)
        # 2. function\(\)   : Captures the text “function()”
        # 3. \(\)           : Captures empty parentheses “()” that often appear in method code
        # 4. Test\.all      : Captures specific text “Test.allTheThings” (a known bug)
        bad_patterns = [r"<.*?>", r"function\(\)", r"\(\)", r"Test\.all"]

        for index, item in enumerate(all_items):
            print(f"Checking Items {index+1}: {item['name']}...")

            #First, validate images not broken
            if not self.inventory_page.check_image_loaded(item['image_element']):
                errors.append(f"FAILED: Images broken for items '{item['name']}'")

            #Second, validate price must be show and had "$" symbols
            if "$" not in item['prices']:
                errors.append(f"FAILED: Incorrect Price Format on the '{item['name']}': {item['prices']}")
            
            #Third and Fourth, Validate the content (Title and Descriptions)
            #Looping pattern for checking two fields in one run
            for pattern in bad_patterns:
                #Description Checking
                if re.search(pattern, item['descriptions']):
                    errors.append(f"BUG FOUND: HTML/Code show in descriptions '{item['name']}', {item['descriptions']}")
                
                #Title Checking
                if re.search(pattern, item['name']):
                    errors.append(f"BUG FOUND: HTML/Code show in descriptions '{item['name']}'")
        
        #FINAL ASSERTIONS
        if errors:
            print("\n=======BUG FOUND=======")
            for err in set(errors):
                print(err)
            print("=========================")
            self.fail(f"FAILED TEST! Because {len(errors)} Problems in the UI")


    def test_8_click_image(self):
        """Case8: Validate if user clicking image it will redirect to product/item details"""
        print("Clicking first product image...")
        self.inventory_page.click_item_image_by_index(0)
        self.assertIn("inventory-item.html", self.driver.current_url, "FAILED/INCORRECT NAVIGATION")

    def test_9_click_title(self):
        """Case9: Validate if user clicking title it will redirect to product/item details"""
        self.inventory_page.click_item_title_by_index(0)
        self.assertIn("inventory-item.html", self.driver.current_url, "FAILED/INCORRECT NAVIGATION")

# --- (AUTO RUNNER) ---
if __name__ == "__main__":

    # pytest options
    pytest_args = [
        __file__,                                  # running this file
        "--html=Report_Test/Report_Inventory.html", # HTML Report to this folder
        "--self-contained-html",                   
        "-v"                                       
    ]

    print("Running...")
    pytest.main(pytest_args)