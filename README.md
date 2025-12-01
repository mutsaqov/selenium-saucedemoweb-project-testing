# 🤖 Selenium Automation Test - SauceDemo E-Commerce
*(Automation Testing Portfolio Project)*

This project implements an exploration of Automation Testing using **Selenium** and **Python**, focusing on the **Page Object Model (POM)** architecture. The goal is to ensure the core functionalities of the SauceDemo web demo run smoothly and stably.

---

### 🗺️ Project Roadmap & Features to be Implemented
The following features are planned for automation coverage in this project:
1. Login (Positive and Negative cases) ✅ **[COMPLETED]** ✅
2. Inventory list page ✅ **[COMPLETED]** ✅
3. Product details ✅ **[COMPLETED]** ✅
4. Checkout item flow
5. Cart ✅ **[COMPLETED]** ✅
6. Logout
7. (Additional) Filtering and Sorting Items ✅ **[COMPLETED]** ✅

---

---

### 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.x
* **Testing Framework:** `unittest` (compatible with `pytest`)
* **Automation Library:** Selenium (Python)
* **Reporting Tool:** `pytest-html`
* **Driver Management:** `webdriver-manager`

### ⚙️ Prerequisites (Local Setup)

Ensure you have Python 3.x installed. Then, install all necessary dependencies using the following command:

```bash
pip install selenium webdriver-manager pytest pytest-html ddt
```
**Library Details:**
1. selenium: Core library for browser automation.
2. webdriver-manager: Automatically manages browser drivers (ChromeDriver).
3. pytest: The testing framework/runner used to execute the tests.
4. pytest-html: Plugin to generate the HTML test reports.
5. ddt: (Data-Driven Tests) Required for the Login Page test scenarios.

---

---

---
## 📂 Project Structure (Page Object Model)

The project utilizes the POM architecture to separate logic and improve maintainability:


| Folder/File | Description |
| :--- | :--- |
| `pages/` | Contains all Page Object Classes (Locators and Actions). |
| `tests/` | Contains the Test Cases (Scenarios and Assertions). |
| `README.md` | This project documentation file. |
| `Report_Test/` | Contains the generated HTML Test Reports. |


---

---

## 💾 Data Management (Data-Driven Testing)

This project adopts a **Data-Driven Testing (DDT)** approach by externalizing test data into a JSON file (`data/users.json`). Instead of hardcoding credentials and expected results directly inside the Python scripts, the framework reads them dynamically.

**File:** `data/users.json`

```json
{
    "positive_cases": [
        {
            "username": "standard_user",
            "password": "secret_sauce",
            "expected_url_part": "inventory.html"
        }
    ],
    "negative_cases": [
        {
            "username": "locked_out_user",
            "...": "..."
        }
    ]
}
```

### 💡 Why use this approach?

1. **Separation of Concerns:** 
    It decouples the Test Logic (Python code) from the Test Data (JSON). If a password changes or a new user is added, we only update the JSON file without touching the codebase.

2. **Scalability & Coverage:** 
    We can easily test 100 different inputs just by adding lines to the JSON file, without writing a single new line of Python code. The @ddt decorator in the test script will automatically iterate through all entries.

3. **Reusability:** 
    The same dataset in `users.json` is reused across different parts of the framework:

    - **`base_test.py:`** Uses the first valid user to perform the automatic login setup.

    - **`test_login_page.py:`** Iterates through the list to test various positive and negative scenarios.

4. **Future Proofing:**

    - **Multi-Role Testing:** Easily manage data for different roles (e.g., `admin`, `guest`, `customer`) in one place.
    - **Localization/Internalization:** If the web app supports multiple languages, we can store expected error messages for each language in the JSON (e.g.,` "error_en"`, `"error_id"`).

---

---

## 📦 Feature 1: Login Test Scenarios (`tests/test_login.py`)

This module handles the login page scenarios, covering comprehensive test scenarios Positive and Negative Cases


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
    Used to validate images. Instead of just checking if the element exists, I use JS (return arguments[0].naturalWidth > 0) to ensure the image is actually rendered by the browser.

5. **Dynamic XPath Locator:**
    A strategy to locate "Add to Cart" buttons based on the product name without hardcoding IDs.

```bash
f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
```

6. **Soft Assertion Logic:**
    In Content Validation, the script collects all errors found in a list (errors.append) instead of stopping at the first failure. This allows checking 6 products in one go and reporting multiple bugs simultaneously.

---

---

### 🐛 Known Issues & Bugs Found
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

### 📋 Test Scenarios Covered (`tests/product_detail_test.py`)


| Test Case ID | Scenario | Description & Validation |
| :--- | :--- | :--- |
| **TC-01** | Navigation to Detail | Verifies that clicking a product title on Inventory page correctly redirects to the Product Detail page. |
| **TC-02** | UI Content Validation | Verifies that the detail page displays the correct Product Name, Description, Price, and Image. |
| **TC-03** | Add & Remove Cart | Verifies the "Add to Cart" and "Remove" button logic, including button text changes and cart badge updates. |
| **TC-04** | Back to Products | Verifies that the "Back to products" button functions correctly and returns user to the inventory list. |


---

---

## 📦 Feature 4: Cart Page Functionality (`tests/cart_test.py`)

This module validates the core functionality of the Shopping Cart, ensuring data consistency between the Inventory and Cart pages, as well as validating the checkout flow and removal logic.


| Test Case ID | Scenario | Description & Validation |
| :--- | :--- | :--- |
| **TC-01** | Access Cart Page | Verifies that clicking the cart icon redirects the user to `cart.html` with the correct page title. |
| **TC-02** | Empty Cart UI | Verifies that the cart list is empty when no items have been added. |
| **TC-03** | Cart Button Visibility | Verifies that "Continue Shopping" and "Checkout" buttons are visible even when the cart is empty. |
| **TC-04** | Validate Added Items | Verifies that the number of items in the list matches the number of items added from Inventory. |
| **TC-05** | Data Consistency | Dynamic Validation: Verifies that Item Name, Description, Price, and Qty match exactly what was selected in Inventory (No hardcoded data). |
| **TC-06** | Remove Item | Verifies that clicking "Remove" deletes the item from the list and updates the cart badge. |
| **TC-07** | Continue Shopping | Verifies that the "Continue Shopping" button redirects the user back to the Inventory page. |
| **TC-08** | Checkout Navigation | Verifies that clicking "Checkout" redirects the user to the `checkout-step-one.html` page. |
| **TC-09** | [Negative Case] Remove All | Stress Test: Adds multiple items and verifies the logic to remove them one by one until the list is completely empty. |
| **TC-10** | [Negative Case] Empty Checkout | Bug Hunting: Verifies if the "Checkout" button is disabled when the cart is empty. (Currently fails intentionally to report the bug). |



### 🧠 Key Technical Implementations (Cart Module)
For the Cart feature, I implemented several advanced automation patterns to ensure robustness:

1.  **Dynamic Data Fetching (Anti-Flaky Strategy):**
    Instead of hardcoding product names (e.g., "Sauce Labs Backpack"), the script dynamically captures the item name from the Inventory Page during runtime and asserts it against the data found in the Cart Page.

    ```python
     # Capture dynamically from Inventory
     expected_item_name = self.inventory_page.get_item_name_by_index(0)
     # Assert dynamically in Cart
     self.assertEqual(cart_data['name'], expected_item_name)
    ```

2. **State Management with Loop (While Loop):** 
   To validate the system's stability when clearing the cart, I use a `while` loop to continuously check for and remove items until the list is confirmed empty.

   ```python
    while len(self.cart_page.get_all_cart_items()) > 0:
    self.cart_page.click_remove_item_by_index(0)
   ```

3. **Intentional Failure Reporting:** 
   For Negative Case TC-10, i implemented a logic to catch a "Valid Bug" (Checkout enabled on empty cart). The script detects the bug and raises a self.fail() with a specific report message, ensuring the issue is highlighted in the HTML Report without breaking the test execution flow.


### 🐛 Known Issues & Bugs Found


| Bug Type | Feature| Description |
| :--- | :--- | :--- |
| **Logic Flaw** | Cart / Checkout | The "Checkout" button remains enabled and functional even when the cart is empty, allowing users to proceed to the checkout page with 0 items. |


**Note:** Above is known issues, the expected behavior from QA pov is > the Checkout button must be disabled or not show if user doesn't have any list on the cart menu's.


---

## 🚀 How to Run Tests
Execute all test scenarios from your VS Code terminal while in the root project directory:

### For login page test:

```bash
python tests/test_login_page.py
```

### For Inventory page test:

```bash
python tests/test_inventory.py
```

### For Detail Product page test:

```bash
python tests/test_product_detail.py
```

### For Cart page test:

```bash
python tests/cart_test.py
```


---

---

## 📝 Test Reporting

The execution results are automatically saved in HTML format within the `Report_Test/` folder generated by **pytest-html**.

The report uses the `--self-contained-html` argument, meaning the CSS and logs are embedded into a single `.html` file, making it easy to share.

**To view the report:**
1. Navigate to the `Report_Test/` folder.
2. Double-click the generated `.html` file (e.g., `Report_Cart.html`) to view the Pass/Fail details in your browser.

### 🚀 How to Run Test and get the report
1. You can execute the tests directly from your VS Code terminal. << **Recommended way, you only run the test script and the report will automatically generated**
2. Or Using Pytest Command You can also run it using standard pytest commands:

```bash
# Run with HTML Report generation
pytest tests/test_cart.py --html=Report_Test/Report_Cart.html --self-contained-html
```

---