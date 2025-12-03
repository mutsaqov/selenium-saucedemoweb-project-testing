# 🤖 Selenium Automation Test - SauceDemo E-Commerce
*(Automation Testing Portfolio Project)*

This project implements an exploration of Automation Testing using **Selenium** and **Python**, focusing on the **Page Object Model (POM)** architecture. The goal is to ensure the core functionalities of the SauceDemo web demo run smoothly and stably.

---

### 🗺️ Project Roadmap & Features to be Implemented
The following features are planned for automation coverage in this project:
1. Login (Positive and Negative cases) ✅ **[COMPLETED]** ✅
2. Inventory list page ✅ **[COMPLETED]** ✅
3. Product details ✅ **[COMPLETED]** ✅
4. Checkout item ✅ **[COMPLETED]** ✅
5. Cart ✅ **[COMPLETED]** ✅
6. Logout ✅ **[COMPLETED]** ✅
7. (Additional) Filtering and Sorting Items ✅ **[COMPLETED]** ✅

---

---

### 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.x
* **Testing Framework:** `unittest`
* **Automation Library:** Selenium (Python)
* **Reporting Tool:** `html-testRunner`
* **Driver Management:** `webdriver-manager`

### ⚙️ Prerequisites (Local Setup)

Ensure you have Python 3.x installed. Then, install all necessary dependencies using the following command:

```bash
pip install selenium html-testrunner webdriver-manager
```
---

---

### 📂 Project Structure (Page Object Model)

### 📦 Feature 1: Login Functionality
The project utilizes the POM architecture to separate logic and improve maintainability:


| Folder/File | Description |
| :--- | :--- |
| `pages/` | Contains all Page Object Classes (Locators and Actions). Example: `login_page.py` . |
| `tests/` | Contains the Test Cases (Scenarios and Assertions). Example: `test_login_page.py` . |
| `README.md` | This project documentation file. |
| `Report_Test/` | Contains the generated HTML Test Reports. |


This module covers the authentication process, including positive logins and handling various error states.

## 📋 Login Test Scenarios (tests/test_login.py)

| Test Case ID | Scenario | Description & Validation |
| :--- | :--- | :--- |
| **TC-01** | Valid Login | Verify successful login with valid standard_user credentials. |
| **TC-02** | Locked Out User | Verify error message when logging in with locked_out_user. |
| **TC-03** | Invalid Password/username | Verify error message when the password/username is incorrect. |
| **TC-04** | Empty Password Fields | Verify error message when the password fields is empty and hit Login button. |
| **TC-05** | Empty Password and Username Fields | Verify error message when the password and username fields is empty and hit Login button. |

---

---

## 📦 Feature 2 : Inventory & Product Management

This module handles the main product listing page, covering comprehensive test scenarios from UI validation to dynamic "Add to Cart" logic.

### 📋 Test Scenarios Covered (`tests/test_inventory.py`)

| Test Case ID | Scenario | Description & Validation |
| :--- | :--- | :--- |
| **TC-01** | Inventory Display | Ensures the page loads products correctly (Assert item count > 0). |
| **TC-02** | Add Item by Name | Adds specific items (via Dynamic XPath) using a **List Loop** to handle multiple items efficiently. |
| **TC-03** | Add Item by Index | Adds the top 3 items from the list using an **Index Loop** strategy. |
| **TC-04** | Product Sorting | Validates all 4 sorting options (A-Z, Z-A, Low-High, High-Low) using **Dictionary Mapping**. |
| **TC-05** | Cart Navigation | Verifies that clicking the cart icon correctly redirects to `cart.html`. |
| **TC-06** | Sidebar Menu | Verifies that the Burger Menu is clickable and opens the sidebar. |
| **TC-07** | Product List | Verifies item content (Images not broken, descriptions not showing HTML/Code, title not showing HTML/Code, and Price)  |
| **TC-08** | Product List | Verifies user can click product images and redirect to product details  |
| **TC-09** | Product List | Verifies user can click product title and redirect to product details  |

### 🧠 Key Technical Implementations

This feature implements several **Advanced Selenium** techniques:

1.  **Dynamic XPath Locator:**
    A strategy to locate "Add to Cart" buttons based on the product name without hardcoding IDs.
    ```python
    f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
    ```

2.  **Data-Driven Loops:**
    Utilizing Python `Lists` and `Dictionaries` to iterate through test data, reducing code duplication and increasing coverage.

3.  **Dropdown Handling:**
    Using Selenium's `Select` class to interact with and validate the product sorting dropdown menu.

3.  **Regex (Regular Expression) Validation:**
    Used in INV-07 to detect data leaks. The script scans product descriptions and titles for HTML tags (<.*?>) or function calls (e.g., test.allTheThings()), marking them as defects if found.

4. **JavaScript Executor:**
    Used to validate images. Instead of just checking if the element exists, we use JS (return arguments[0].naturalWidth > 0) to ensure the image is actually rendered by the browser.

5. **Dynamic XPath Locator:**
    A strategy to locate "Add to Cart" buttons based on the product name without hardcoding IDs.

```bash
f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
```

6. **Soft Assertion Logic:**
    In Content Validation, the script collects all errors found in a list (errors.append) instead of stopping at the first failure. This allows checking 6 products in one go and reporting multiple bugs simultaneously.

---

---

🐛 Known Issues & Bugs Found
During the execution of automated tests (specifically INV-07), the script successfully caught the following defects on the demo website:


| Bug Type | Product Name | Description |
| :--- | :--- | :--- |
| **Data Leak** | Test.allTheThings() T-Shirt | Product description contains raw HTML tags/code logic. |
| **UI Formatting** | Test.allTheThings() T-Shirt | Title displays function-like syntax, inconsistent with other products. |


**Note:** The test INV-07 is expected to FAIL to highlight these defects.

---

---

## 📦 Feature 3: Product Detail Validation

This module validates the detailed view of a product, ensuring UI consistency and cart functionality from within the item page.

## 📋 Test Scenarios Covered (`tests/product_detail_test.py`)

| Test Case ID | Scenario | Description & Validation |
| :--- | :--- | :--- |
| **TC-01** | Navigation to Detail | Verifies that clicking a product title on Inventory page correctly redirects to the Product Detail page. |
| **TC-02** | UI Content Validation | Verifies that the detail page displays the correct Product Name, Description, Price, and Image. |
| **TC-03** | Add & Remove Cart | Verifies the "Add to Cart" and "Remove" button logic, including button text changes and cart badge updates. |
| **TC-04** | Back to Products | VVerifies that the "Back to products" button functions correctly and returns user to the inventory list. |


---


---

### 🚀 How to Run Tests
Execute all test scenarios from your VS Code terminal while in the root project directory:

For login page test:

```bash
python tests/test_login_page.py
```

For Inventory page test:

```bash
python tests/test_inventory.py
```

For Detail Product pages test:

```bash
python tests/test_product_detail.py
```

---

---

### 📝 Test Reporting
The execution results are automatically saved in HTML format within the Report_Test folder generated by html-testRunner.
1. Navigate to the Report_Test/ folder.
2. Double-click the generated .html file to view the Pass/Fail report in your browser.

---