import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from pages.product_detail_page import sauceDemoProductDetailPage
from pages.inventory_page import sauceDemoInventoryPage
from tests.base_test import BaseTestLoggedIn
import re #<< for checking HTML logic
import pytest

class TestProductDetailPage(BaseTestLoggedIn):
    def setUp(self):
        super().setUp()
        self.product_detail_page = sauceDemoProductDetailPage(self.driver)
        self.inventory_page = sauceDemoInventoryPage(self.driver)  
        
    
    def test_01_DetailProduct_navigateToDetail(self):
        """CASE01: Validate successfully navigate to product detail page"""
        print(f"TEST NAVIGATION & DATA CONSISTENCY")
        
        expected_name = self.product_detail_page.get_product_name_by_index(0)
        print(f"STEP 1: USER CHOOSE 1 PRODUCT '{expected_name}' from product list")
        
        self.product_detail_page.click_item_image_by_index(0)
        self.assertIn("inventory-item.html", self.driver.current_url, "FAILED!")
        
        actual_name = self.detail_page.get_product_name()
        print(f"STEP 2: Detail page showing '{actual_name}'")
        self.assertEqual(expected_name, actual_name, "BUG! PRODUCT NAME IS DIFFRENT")
    
    def test_02_DetailProduct_validateUiComponents(self):
        """Case02: Validate Price, Desc, Back Button, Add to Cart Button Visibility"""
        print("TEST UI COMPONENT VALIDATION")
        
        self.product_detail_page.click_item_title_by_index(0)
        
        is_price_show = self.detail_page.is_price_show()
        print(f"STEP 1: PRICE SHOWING: {is_price_show}")
        self.assertTrue(is_price_show, "BUG! PRICE NOT SHOWING")
        
        is_desc_show = self.detail_page.is_desc_show()
        print(f"STEP 2: DESCRIPTION SHOWING: {is_desc_show}")
        self.assertTrue(is_desc_show, "BUG! DESCRIPTION NOT SHOWING")
        
        is_back_button_show = self.detail_page.is_back_button_show()
        print(f"STEP 3: BACK BUTTON SHOWING: {is_back_button_show}")
        self.assertTrue(is_back_button_show, "BUG! BACK BUTTON NOT SHOWING")
        
        is_add_to_cart_button_show = self.detail_page.is_add_to_cart_button_show()
        print(f"STEP 4: ADD TO CART BUTTON SHOWING: {is_add_to_cart_button_show}")
        self.assertTrue(is_add_to_cart_button_show, "BUG! ADD TO CART BUTTON NOT SHOWING")
        
    def test_03_DetailProduct_validateBackButton(self):
        """Case03: Validate Back Button Functionality"""
        print("TEST BACK BUTTON FUNCTIONALITY")

        self.product_detail_page.click_item_title_by_index(0)

        print("STEP 1: USER CLICK BACK BUTTON")
        self.detail_page.click_back_button()

        self.assertIn("inventory.html", self.driver.current_url, "FAILED!")
    
    def test_04_05_add_remove_cart_logic(self):
        """Case 04: Add to Cart Button Functionality
            Case 05: Remove from Cart Button Functionality"""
            
        self.product_detail_page.click_item_title_by_index(0)
        
        #---STEP 1: ADD TO CART---
        initial_badge = self.product_detail_page.get_cart_value_badge()
        print(f"STEP 1: INITIAL CART BADGE VALUE: {initial_badge}")
        
        print("STEP 2: USER CLICK ADD TO CART BUTTON")
        self.detail_page.click_add_to_cart_or_remove_button()
        
        #Validation 1: Badge value increased
        new_badge = self.product_detail_page.get_cart_value_badge()
        self.assertEqual(initial_badge + 1, new_badge, "BUG! BADGE VALUE NOT INCREASED")
        
        #Validation 2: Remove button is showing
        btn_text = self.detail_page.get_add_to_cart_button_text()
        self.assertEqual(btn_text, "REMOVE", "BUG! BUTTON TEXT NOT CHANGED TO REMOVE")
        
        #---STEP 2: REMOVE FROM CART---
        print("STEP 3: USER CLICK REMOVE BUTTON")
        self.detail_page.click_add_to_cart_or_remove_button()

        #Validation 1: Badge value decreased
        final_badge = self.product_detail_page.get_cart_value_badge()
        self.assertEqual(initial_badge, final_badge, "BUG! BADGE VALUE NOT DECREASED")

        #Validation 2: Add to cart button is showing
        final_btn_text = self.detail_page.get_add_to_cart_button_text()
        self.assertEqual(final_btn_text, "ADD TO CART", "BUG! BUTTON TEXT NOT CHANGED TO ADD TO CART")

# --- (AUTO RUNNER) ---
if __name__ == "__main__":

    # pytest options
    pytest_args = [
        __file__,                                  # running this file
        "--html=Report_Test/Report_Detail_Product.html", # HTML Report to this folder
        "--self-contained-html",                   
        "-v"                                       
    ]

    print("Running...")
    pytest.main(pytest_args)
