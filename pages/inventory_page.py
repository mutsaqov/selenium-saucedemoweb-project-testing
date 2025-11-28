from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class sauceDemoInventoryPage:

    #LOCATORS
    PAGE_TITLE              = (By.CLASS_NAME, "title")

    OPEN_SIDEBAR_MENU       = (By.ID, "react-burger-menu-btn")
    CLOSE_SIDEBAR_MENU      = (By.ID, "react-burger-cross-btn")

    PRODUCT_SORTING         = (By.CLASS_NAME, "product_sort_container")
    SHOPPING_CART           = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE     = (By.CLASS_NAME, "shopping_cart_badge")

    INVENTORY_ITEMS         = (By.CLASS_NAME, "inventory_item")
    ALL_ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory") #<-- Locator for all button add to card

    ITEM_IMAGES             = (By.CSS_SELECTOR, "img.inventory_item_img")
    ITEM_NAMES              = (By.CLASS_NAME, "inventory_item_name ")
    ITEM_DESCRIPTIONS       = (By.CLASS_NAME, "inventory_item_desc")
    ITEM_PRICE              = (By.CLASS_NAME, "inventory_item_price")

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
        
    def get_all_items_data(self):
        """
        Get all items data (Title, Description, Price, and Image) in one loop
        RETURN: LIST OF DICTIONARIES
        """
        # FIND_ELEMENTS (Bulk/Plural) -> Returning LIST
        # names = [Element_Title_1, Element_Title_2, Element_Title_3, ...]
        items = self.wait.until(EC.visibility_of_all_elements_located(self.INVENTORY_ITEMS))
        names = self.driver.find_elements(*self.ITEM_NAMES)
        descriptions = self.driver.find_elements(*self.ITEM_DESCRIPTIONS)
        prices = self.driver.find_elements(*self.ITEM_PRICE)
        images = self.driver.find_elements(*self.ITEM_IMAGES)
        
        results = []

        #looping as many times as the number of items
        for i in range(len(names)):
            data = {
                "name": names[i].text,
                "descriptions": descriptions[i].text,
                "prices": prices[i].text,
                "image_element": images[i], # Save images element for checking later
                "name_element": images[i] #Save name element for click actions
            }
            results.append(data)

        return results
    
    def check_image_loaded(self, image_element):
        """
        Check are all images broken or not using java script
        RETURN: True if all images is good
        """
        return self.driver.execute_script(
            "return arguments[0].complete && typeof arguments[0].naturalWidth != 'undefined' && arguments[0].naturalWidth > 0",
            image_element
        )
    
    def click_item_image_by_index(self, index):
        """Click on the product images in order """
        images = self.wait.until(EC.visibility_of_all_elements_located(self.ITEM_IMAGES))
        #Choose one of them based on order number (index)
        images[index].click()
    
    def click_item_title_by_index(self, index):
        """Click on the product titles in order"""
        title = self.wait.until(EC.visibility_of_all_elements_located(self.ITEM_NAMES))
        title[index].click()
        
    def get_item_name_by_index(self, index):
        """Get item name by index without clicking"""
        names = self.wait.until(EC.visibility_of_all_elements_located(self.ITEM_NAMES))
        return names[index].text
        

