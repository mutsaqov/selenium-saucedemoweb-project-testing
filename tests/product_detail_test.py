import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pages.inventory_page import sauceDemoInventoryPage
from pages.product_detail_page import sauceDemoProductDetailPage 
from tests.base_test import BaseTestLoggedIn
import pytest

class TestProductDetailPage(BaseTestLoggedIn):
    def setUp(self):
        super().setUp()
        self.inventory_page = sauceDemoInventoryPage(self.driver)
        self.product_detail_page = sauceDemoProductDetailPage(self.driver)
        
        self.logger.info("--- Product Detail Page Test Started ---")
    
    def test_01_DetailProduct_navigateToDetail(self):
        """CASE01: Validate successfully navigate to product detail page"""
        self.logger.info("Scenario: Navigation & Data Consistency Check")
        
        # 1. Get Expected Name from Inventory
        expected_name = self.inventory_page.get_item_name_by_index(0)
        self.logger.info(f"STEP 1: USER CHOOSE 1 PRODUCT '{expected_name}' from product list")
        
        self.inventory_page.click_item_title_by_index(0)
        # 2. Validate URL
        try:
            self.assertIn("inventory-item.html", self.driver.current_url)
            self.logger.info("PASSED: URL redirect correct.")
        except AssertionError as e:
            self.logger.error(f"FAILED: URL mismatch. Got {self.driver.current_url}")
            raise e
        
        #3. Validate Product Name matches
        actual_name = self.product_detail_page.get_product_name()
        self.logger.info(f"STEP 2: Detail page showing '{actual_name}'")
        
        try:
            self.assertEqual(expected_name, actual_name)
            self.logger.info("PASSED: Product Name is consistent.")
        except AssertionError as e:
            self.logger.error(f"BUG! Product Name Mismatch. Expected '{expected_name}', Got '{actual_name}'")
            raise e
    
    def test_02_DetailProduct_validateUiComponents(self):
        """Case02: Validate Price, Desc, Back Button, Add to Cart Button Visibility"""
        self.logger.info("Scenario: UI Component Validation (Price, Desc, Buttons)")
        
        self.inventory_page.click_item_title_by_index(0)
        
        #Validate Components
        components = {
            "Price": self.product_detail_page.is_price_displayed,
            "Description": self.product_detail_page.is_description_displayed,
            "Back Button": self.product_detail_page.is_back_button_displayed,
            "Add to Cart Button": self.product_detail_page.is_add_to_cart_button_displayed
        }
        
        for name, check_func in components.items():
            is_visible = check_func()
            if is_visible:
                self.logger.info(f"SUCCESS: {name} is visible.")
            else:
                self.logger.error(f"BUG! {name} is NOT visible.")
                self.fail(f"UI Element Missing: {name}")
        
    def test_03_DetailProduct_validateBackButton(self):
        """Case03: Validate Back Button Functionality"""
        self.logger.info("Scenario: Back Button Functionality")

        self.inventory_page.click_item_title_by_index(0)

        self.logger.info("STEP 1: USER CLICK BACK BUTTON")
        self.product_detail_page.click_back_button()

        try:
            self.assertIn("inventory.html", self.driver.current_url)
            self.logger.info("PASSED: Redirected back to Inventory Page.")
        except AssertionError as e:
            self.logger.error(f"FAILED: Navigation failed. Current URL: {self.driver.current_url}")
            raise e
    
    def test_04_05_add_remove_cart_logic(self):
        """Case 04: Add to Cart Button Functionality
            Case 05: Remove from Cart Button Functionality"""
        self.logger.info("Scenario: Add/Remove Cart Logic on Detail Page")
        
        self.inventory_page.click_item_title_by_index(0)
        
        #---STEP 1: ADD TO CART---
        initial_badge = self.product_detail_page.get_cart_value_badge()
        self.logger.info(f"STEP 1: INITIAL CART BADGE VALUE: {initial_badge}")
        
        self.logger.info("STEP 2: USER CLICK ADD TO CART BUTTON")
        self.product_detail_page.click_add_to_cart_or_remove_button()
        
        #Validation 1: Badge value increased
        new_badge = self.product_detail_page.get_cart_value_badge()
        if new_badge == initial_badge + 1:
            self.logger.info(f"SUCCESS: Badge increased to {new_badge}")
        else:
            self.logger.error(f"ERROR! Badge value did not increase. Got {new_badge}")
            self.fail("Cart Badge Failed to Update (Add)")
        
        #Validation 2: Remove button is showing
        btn_text = self.product_detail_page.get_add_to_cart_button_text()
        if btn_text == "Remove":
            self.logger.info("SUCCESS: Button text changed to 'Remove'")
        else:
            self.logger.remove(f"ERROR! Button text did not change. Got '{btn_text}'")
            self.fail("Button Text Failed to Update")
            
        #---STEP 2: REMOVE FROM CART---
        self.logger.info("STEP 3: USER CLICK REMOVE BUTTON")
        self.product_detail_page.click_add_to_cart_or_remove_button()

        #Validation 1: Badge value decreased
        final_badge = self.product_detail_page.get_cart_value_badge()
        if final_badge == initial_badge:
            self.logger.info(f"PASSED: Badge reset to {final_badge}")
        else:
            self.logger.error(f"BUG! Badge value did not decrease. Got {final_badge}")
            self.fail("Cart Badge Failed to Update (Remove)")

        #Validation 2: Add to cart button is showing
        final_btn_text = self.product_detail_page.get_add_to_cart_button_text()
        if final_btn_text == "Add to cart":
            self.logger.info("PASSED: Button text reverted to 'Add to cart'")
        else:
            self.logger.error(f"BUG! Button text did not revert. Got '{final_btn_text}'")
            self.fail("Button Text Failed to Revert")

# --- (AUTO RUNNER) ---
if __name__ == "__main__":

    # pytest options
    pytest_args = [
        __file__,                                  # running this file
        "--html=Report_Test/Report_Detail_Product.html", # HTML Report to this folder
        "--self-contained-html",                   
        "-v"                                       
    ]
    pytest.main(pytest_args)
