from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class sauceDemoCheckoutPage:

    #LOCATORS
    #Information page locators:
    CHECKOUT_PAGE_TITLE    = (By.CLASS_NAME, "title")
    INPUT_FIRST_NAME       = (By.ID, "first-name")
    INPUT_LAST_NAME        = (By.ID, "last-name")
    INPUT_POSTAL_CODE      = (By.ID, "postal-code")
    BTN_CONTINUE           = (By.ID, "continue")
    BTN_CANCEL             = (By.ID, "cancel")
    ERROR_MESSAGE          = (By.CSS_SELECTOR, "h3[data-test='error']") 

    #Overview page locators:
    SUMMARY_ITEM_PRICE    = (By.CLASS_NAME, "inventory_item_price")
    SUMMARY_SUBTOTAL      = (By.CLASS_NAME, "summary_subtotal_label")
    SUMMARY_TAX           = (By.CLASS_NAME, "summary_tax_label")
    SUMMARY_TOTAL         = (By.CLASS_NAME, "summary_total_label")
    BTN_FINISH            = (By.ID, "finish")

    #completed page locators:
    COMPLETED_HEADER      = (By.CLASS_NAME, "complete-header")
    BTN_BACK_HOME         = (By.ID, "back-to-products")

    #CONSTRUCTOR
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    #ACTIONS
    def get_page_title(self):
        """Get Page Title Text"""
        element = self.wait.until(EC.visibility_of_element_located(self.CHECKOUT_PAGE_TITLE))
        return element.text
    
    #INFORMATION PAGE ACTIONS
    def fill_information(self, fname, lname, postalcode):
        if fname is not None:
            self.driver.find_element(*self.INPUT_FIRST_NAME).send_keys(fname)
        if lname is not None:
            self.driver.find_element(*self.INPUT_LAST_NAME).send_keys(lname)
        if postalcode is not None:
            self.driver.find_element(*self.INPUT_POSTAL_CODE).send_keys(postalcode)
    
    def click_continue(self):
        element = self.driver.find_element(*self.BTN_CONTINUE)
        element.click()
    
    def click_cancel(self):
        element = self.driver.find_element(*self.BTN_CANCEL)
        element.click()
    
    def get_error_message(self):
        element = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return element.text
    
    def verify_fields_visible(self):
        return (
            self.driver.find_element(*self.INPUT_FIRST_NAME).is_displayed() and
            self.driver.find_element(*self.INPUT_LAST_NAME).is_displayed() and
            self.driver.find_element(*self.INPUT_POSTAL_CODE).is_displayed()
        )
    
    #INVOICE OVERVIEW PAGE ACTIONS
    def get_item_prices_as_float(self):
        price_elements = self.driver.find_elements(*self.SUMMARY_ITEM_PRICE)
        prices = []
        #This logic will eliminate the $ sign and convert to float
        #examples from $30.12 > 30.12
        for p in price_elements:
            price_text = p.text.replace("$", "") #remove $ sign > "30.12"
            prices.append(float(price_text)) #become float 30.12
        return prices

    def get_summary_values(self):
        def parse_price(text):
            match = re.search(r"(\d+\.\d+)", text)
            return float(match.group(1)) if match else 0.0

        subtotal_text = self.driver.find_element(*self.SUMMARY_SUBTOTAL).text
        tax_text = self.driver.find_element(*self.SUMMARY_TAX).text
        total_text = self.driver.find_element(*self.SUMMARY_TOTAL).text

        return{
            "subtotal": parse_price(subtotal_text),
            "tax": parse_price(tax_text),
            "total": parse_price(total_text)
        }
    
    def click_finish(self):
        element = self.driver.find_element(*self.BTN_FINISH)
        element.click()

    #COMPLETED PAGE ACTIONS
    def get_completed_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.COMPLETED_HEADER)).text
    
    def click_back_home(self):
        element = self.driver.find_element(*self.BTN_BACK_HOME)
        element.click()

    