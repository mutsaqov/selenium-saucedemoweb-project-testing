from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class sauceDemoProductDetailPage:
    
    #LOCATORS
    DETAIL_NAME = (By.CLASS_NAME, "inventory_details_name")
    DETAIL_DESCRIPTION = (By.CLASS_NAME, "inventory_details_desc")
    DETAIL_PRICE = (By.CLASS_NAME, "inventory_details_price")
    DETAIL_IMAGE = (By.CLASS_NAME, "inventory_details_img")
    ADD_TO_CART_BUTTON_OR_REMOVE = (By.CLASS_NAME, "btn_inventory") 
    BACK_BUTTON = (By.ID, "back-to-products")
    
    BTN_INVENTORY = (By.CLASS_NAME, "btn_inventory")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    
    #CONSTRUCTOR
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
    def get_product_name(self):
        element = self.wait.until(EC.visibility_of_element_located(self.DETAIL_NAME))
        return element.text
    
    def is_price_displayed(self):
        element = self.wait.until(EC.visibility_of_element_located(self.DETAIL_PRICE))
        return element.is_displayed()
    
    def is_image_displayed(self):
        try:
            element = self.wait.until(EC.visibility_of_element_located(self.DETAIL_IMAGE))
            return self.driver.execute_script("return arguments[0].complete && typeof arguments[0].naturalWidth != 'undefined' && arguments[0].naturalWidth > 0;", 
                                            element) 
        except:
            return False
        
    def is_description_displayed(self):
        element = self.wait.until(EC.visibility_of_element_located(self.DETAIL_DESCRIPTION))
        return element.is_displayed()

    def is_back_button_displayed(self):
        element = self.wait.until(EC.visibility_of_element_located(self.BACK_BUTTON))
        return element.is_displayed()
    
    def click_back_button(self):
        element = self.wait.until(EC.element_to_be_clickable(self.BACK_BUTTON))
        element.click()

    def is_add_to_cart_button_displayed(self):
        element = self.wait.until(EC.visibility_of_element_located(self.ADD_TO_CART_BUTTON_OR_REMOVE))
        return element.is_displayed()
    
    def click_add_to_cart_or_remove_button(self):
        """Click the add to cart button is depend what the status show ADD TO CART or REMOVE"""
        element = self.wait.until(EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON_OR_REMOVE))
        element.click()
        
    def get_add_to_cart_button_text(self):
        element = self.wait.until(EC.visibility_of_element_located(self.ADD_TO_CART_BUTTON_OR_REMOVE))
        return element.text
    
    def get_cart_value_badge(self):
        try:
            short_wait = WebDriverWait(self.driver, 2)
            element = short_wait.until(EC.visibility_of_element_located(self.SHOPPING_CART_BADGE))
            return int(element.text)
        except:
            return 0
    