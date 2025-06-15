import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string

# Constants
BASE_URL = "http://localhost:5000"
TEST_USERNAME = f"testuser_{random.randint(1000, 9999)}"
TEST_EMAIL = f"{TEST_USERNAME}@test.com"
TEST_PASSWORD = "TestPassword123"
ITEM_NAME = f"Test Item {random.randint(1000, 9999)}"
ITEM_DESCRIPTION = "This is a test item created by Selenium"
ITEM_QUANTITY = "5"
UPDATED_ITEM_NAME = f"Updated Item {random.randint(1000, 9999)}"

@pytest.fixture
def driver():
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Create a new instance of the Chrome driver
    browser = webdriver.Chrome(options=chrome_options)
    
    yield browser
    
    # Teardown - Close the browser
    browser.quit()

def test_01_home_page_redirects_to_login(driver):
    """Test case 1: Check if the home page redirects to login when not authenticated"""
    driver.get(BASE_URL)
    
    # Check if redirected to login page
    assert "Login" in driver.title
    
    # Verify login form exists
    login_form = driver.find_element(By.TAG_NAME, "form")
    assert login_form is not None

def test_02_register_new_user(driver):
    """Test case 2: Register a new user"""
    driver.get(f"{BASE_URL}/register")
    
    # Fill out the registration form
    driver.find_element(By.ID, "username").send_keys(TEST_USERNAME)
    driver.find_element(By.ID, "email").send_keys(TEST_EMAIL)
    driver.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
    
    # Submit the form
    driver.find_element(By.TAG_NAME, "form").submit()
    
    # Check if registration was successful (redirected to login page)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    )
    
    assert "Login" in driver.title
    success_message = driver.find_element(By.CLASS_NAME, "alert-success").text
    assert "Registration successful" in success_message

def test_03_login_with_invalid_credentials(driver):
    """Test case 3: Test login failure with wrong credentials"""
    driver.get(f"{BASE_URL}/login")
    
    # Fill out the login form with invalid credentials
    driver.find_element(By.ID, "username").send_keys("wrong_username")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    
    # Submit the form
    driver.find_element(By.TAG_NAME, "form").submit()
    
    # Check if login failed
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
    )
    
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Invalid username or password" in error_message

def test_04_login_with_valid_credentials(driver):
    """Test case 4: Validate successful login with correct credentials"""
    driver.get(f"{BASE_URL}/login")
    
    # Fill out the login form
    driver.find_element(By.ID, "username").send_keys(TEST_USERNAME)
    driver.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
    
    # Submit the form
    driver.find_element(By.TAG_NAME, "form").submit()
    
    # Check if login was successful
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    
    # Verify we are on the home page
    welcome_message = driver.find_element(By.TAG_NAME, "h1").text
    assert f"Welcome, {TEST_USERNAME}" in welcome_message

def test_05_add_new_item(driver):
    """Test case 5: Add a new inventory item"""
    # Login first
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.ID, "username").send_keys(TEST_USERNAME)
    driver.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
    driver.find_element(By.TAG_NAME, "form").submit()
    
    # Navigate to the add item page
    driver.get(f"{BASE_URL}/add_item")
    
    # Fill out the form
    driver.find_element(By.ID, "name").send_keys(ITEM_NAME)
    driver.find_element(By.ID, "description").send_keys(ITEM_DESCRIPTION)
    driver.find_element(By.ID, "quantity").clear()
    driver.find_element(By.ID, "quantity").send_keys(ITEM_QUANTITY)
    
    # Submit the form
    driver.find_element(By.TAG_NAME, "form").submit()
    
    # Check if item was added successfully
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    )
    
    success_message = driver.find_element(By.CLASS_NAME, "alert-success").text
    assert "Item added successfully" in success_message
    
    # Verify the item appears in the table
    table = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table"))
    )
    assert ITEM_NAME in table.text

def test_06_edit_item(driver):
    """Test case 6: Edit an existing inventory item"""
    # Login first
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.ID, "username").send_keys(TEST_USERNAME)
    driver.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
    driver.find_element(By.TAG_NAME, "form").submit()
    
    # Find the Edit button for the item we just added
    edit_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{ITEM_NAME}')]/following-sibling::td/a[contains(@class, 'btn-warning')]"))
    )
    edit_button.click()
    
    # Edit the item details
    name_field = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "name"))
    )
    name_field.clear()
    name_field.send_keys(UPDATED_ITEM_NAME)
    
    # Submit the form
    driver.find_element(By.TAG_NAME, "form").submit()
    
    # Check if item was updated successfully
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    )
    
    success_message = driver.find_element(By.CLASS_NAME, "alert-success").text
    assert "Item updated successfully" in success_message
    
    # Verify the updated item appears in the table
    table = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table"))
    )
    assert UPDATED_ITEM_NAME in table.text

def test_07_search_functionality(driver):
    """Test case 7: Test search functionality"""
    # Login first
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.ID, "username").send_keys(TEST_USERNAME)
    driver.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
    driver.find_element(By.TAG_NAME, "form").submit()
    
    # Search for the updated item
    search_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "search_term"))
    )
    search_input.send_keys(UPDATED_ITEM_NAME)
    
    # Submit the search form
    search_form = driver.find_element(By.XPATH, "//form[@action='/search']")
    search_form.submit()
    
    # Check if search results page loaded correctly
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Search Results")
    )
    
    # Verify search results contain our item
    table = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "table"))
    )
    assert UPDATED_ITEM_NAME in table.text

def test_08_delete_item(driver):
    """Test case 8: Delete an inventory item"""
    # Login first
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.ID, "username").send_keys(TEST_USERNAME)
    driver.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
    driver.find_element(By.TAG_NAME, "form").submit()
    
    # Find the delete button for the item
    delete_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{UPDATED_ITEM_NAME}')]/following-sibling::td/a[contains(@class, 'btn-danger')]"))
    )
    
    # To handle the confirm dialog
    driver.execute_script("window.confirm = function(){return true;}")
    
    # Click delete button
    delete_button.click()
    
    # Check if item was deleted successfully
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    )
    
    success_message = driver.find_element(By.CLASS_NAME, "alert-success").text
    assert "Item deleted successfully" in success_message

def test_09_update_profile(driver):
    """Test case 9: Update user profile"""
    # Login first
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.ID, "username").send_keys(TEST_USERNAME)
    driver.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
    driver.find_element(By.TAG_NAME, "form").submit()
    
    # Navigate to profile page
    driver.find_element(By.XPATH, "//a[contains(text(), 'Profile')]").click()
    
    # Update email
    updated_email = f"updated_{TEST_EMAIL}"
    email_field = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_field.clear()
    email_field.send_keys(updated_email)
    
    # Submit the form
    driver.find_element(By.TAG_NAME, "form").submit()
    
    # Check if profile was updated successfully
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
    )
    
    success_message = driver.find_element(By.CLASS_NAME, "alert-success").text
    assert "Profile updated successfully" in success_message

def test_10_logout_functionality(driver):
    """Test case 10: Logout functionality"""
    # Login first
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.ID, "username").send_keys(TEST_USERNAME)
    driver.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
    driver.find_element(By.TAG_NAME, "form").submit()
    
    # Click logout link
    logout_link = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Logout')]"))
    )
    logout_link.click()
    
    # Check if logout was successful
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-info"))
    )
    
    info_message = driver.find_element(By.CLASS_NAME, "alert-info").text
    assert "You have been logged out" in info_message
    
    # Verify redirected to login page
    assert "Login" in driver.title
