from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class sauceDemoInventoryPage:

    #LOCATORS
    PAGE_TITLE = (By.CLASS_NAME, "title")

    OPEN_SIDEBAR_MENU = (By.ID, "react-burger-menu-btn")
    CLOSE_SIDEBAR_MENU  = (By.ID, "react-burger-cross-btn")

    PRODUCT_SORTING = (By.CLASS_NAME, "product_sort_container")
    SHOPPING_CART = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ALL_ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory") #<-- Locator for all button add to card

    #CONSTRUCTOR
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    #ACTIONS
    def get_page_title(self):
        element = self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        return element.text
    
    
    def click_sidebar_menu(self):
        element = self.wait.until(EC.element_to_be_clickable(self.OPEN_SIDEBAR_MENU))
        element.click()

    def click_cart_icon(self):
        element = self.wait.until(EC.element_to_be_clickable(self.SHOPPING_CART))
        element.click()
    
    def get_cart_badge_value(self):
        #get cart badge value if 0, do RETURN
        try:
            short_wait = WebDriverWait(self.driver, 2)
            element = short_wait.until(EC.visibility_of_element_located(self.SHOPPING_CART_BADGE))
            return int(element.text)
        except:
            return 0
    
    def get_inventory_count(self):
        element = self.wait.until(EC.visibility_of_all_elements_located(self.INVENTORY_ITEMS))
        return len(element)
    
    def product_sorting(self, option_value):
        element = self.wait.until(EC.visibility_of_element_located(self.PRODUCT_SORTING))
        select = Select(element)
        select.select_by_value(option_value)

    def get_active_sort_option(self):
        """ Retrieve text from the currently 
        selected option in the dropdownExample: 
        Return “Name (A to Z)” 
        """
        element = self.wait.until(EC.visibility_of_element_located(self.PRODUCT_SORTING))
        select = Select(element)
        return select.first_selected_option.text

    def add_item_by_name(self, item_name):
        xpath_dynamic = f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_dynamic))).click()
    
    def add_item_by_index(self, index):
        buttons = self.wait.until(EC.visibility_of_all_elements_located(self.ALL_ADD_TO_CART_BUTTONS))
        if index < len(buttons):
            buttons[index].click()
        else:
            raise Exception(f"Item index {index} not found!")
        
