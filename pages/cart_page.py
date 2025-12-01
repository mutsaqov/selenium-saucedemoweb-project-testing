from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class sauceDemoCartPage:
    
    #LOCATORS
    CART_PAGE_TITLE     = (By.CLASS_NAME, "title")
    CART_ITEM           = (By.CLASS_NAME, "cart_item")
    CART_BADGE          = (By.CLASS_NAME, "shopping_cart_badge")
    
    ITEM_QUANTITY       = (By.CLASS_NAME, "cart_quantity")
    ITEM_NAME           = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE          = (By.CLASS_NAME, "inventory_item_price")   
    ITEM_DESCRIPTION    = (By.CLASS_NAME, "inventory_item_desc")    
    BTN_REMOVE_ITEM     = (By.XPATH, "//button[contains(text(), 'Remove')]")
    
    BTN_CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    BTN_CHECKOUT        = (By.ID, "checkout")
    
    
    # CONSTRUCTOR
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    #ACTIONS
    def get_page_title(self):
        element = self.wait.until(EC.visibility_of_element_located(self.CART_PAGE_TITLE))
        return element.text
    
    def get_all_cart_item(self):
        """Return list of element all item in cart"""
        try:
            return self.driver.find_elements(*self.CART_ITEM)
        except:
            return []

    def get_item_data_by_index(self, index):
        """Get Text Data (QTY, NAME, DESC, PRICE) FROM ITEM BY INDEX"""
        items = self.get_all_cart_item()
        if not items:
            raise Exception("CART IS EMPTY!")
        
        item = items[index]
        return{
            "quantity": item.find_element(*self.ITEM_QUANTITY).text,
            "name": item.find_element(*self.ITEM_NAME).text,
            "description": item.find_element(*self.ITEM_DESCRIPTION).text,
            "price": item.find_element(*self.ITEM_PRICE).text
        }
    
    def click_remove_item_by_index(self, index):
        """Click Remove Button on Item by Index"""
        items = self.get_all_cart_item()
        item = items[index]
        button_remove = item.find_element(*self.BTN_REMOVE_ITEM)
        button_remove.click()
        
    def click_continue_shopping(self):
        element = self.wait.until(EC.element_to_be_clickable(self.BTN_CONTINUE_SHOPPING))
        element.click()

    def click_checkout(self):
        element = self.wait.until(EC.element_to_be_clickable(self.BTN_CHECKOUT))
        element.click()
        
    def is_checkout_enabled(self):
        """Check if checkout button is enabled"""
        btn = self.driver.find_element(*self.BTN_CHECKOUT)
        return btn.is_enabled()