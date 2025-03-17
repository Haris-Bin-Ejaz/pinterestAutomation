import csv
import os
import time
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from utils.fake_data import generate_fake_user  # Import Fake Data Generator


# **🔹 Setup WebDriver**
def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# **🔹 Click Signup Button**
def click_signup_button(driver):
    try:
        signup_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-test-id='simple-signup-button']//button"))
        )
        signup_button.click()
        print("✅ Signup button clicked successfully!")
    except Exception as e:
        print(f"❌ Error clicking signup button: {e}")


# **🔹 Click Business Account Button**
def click_business_account_button(driver):
    try:
        business_account_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Create a free business account')]"))
        )
        business_account_button.click()
        print("✅ 'Create a Free Business Account' button clicked successfully!")
    except Exception as e:
        print(f"❌ Error clicking business account button: {e}")


# **🔹 Clear & Enter Text**
def clear_and_enter_text(field, text):
    try:
        field.send_keys(Keys.CONTROL + "a")
        field.send_keys(Keys.DELETE)
        field.send_keys(text)
    except Exception as e:
        print(f"❌ Error clearing and entering text: {e}")


# **🔹 Enter Email**
def enter_email(driver, email):
    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        clear_and_enter_text(email_field, email)
        print(f"✅ Email entered: {email}")
    except Exception as e:
        print(f"❌ Error entering email: {e}")


# **🔹 Enter Password**
def enter_password(driver, password):
    try:
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        clear_and_enter_text(password_field, password)
        print(f"✅ Password entered: {password}")
    except Exception as e:
        print(f"❌ Error entering password: {e}")


# **🔹 Enter Birthdate**
def enter_birthdate(driver, birthdate):
    try:
        birthdate_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "birthdate"))
        )
        clear_and_enter_text(birthdate_field, birthdate)
        print(f"✅ Birthdate entered: {birthdate}")
    except Exception as e:
        print(f"❌ Error entering birthdate: {e}")


# **🔹 Click 'Create Account' Button**
def click_create_account_button(driver):
    try:
        create_account_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(., 'Create account')]"))
        )
        create_account_button.click()
        print("✅ 'Create account' button clicked successfully!")
    except Exception as e:
        print(f"❌ Error clicking 'Create account' button: {e}")


# **🔹 Verify Element Exists**
def verify_element_exists(driver, by, value):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        print(f"✅ Element found: {value}")
        return element
    except:
        print(f"❌ Element not found: {value}")
        return None


# **🔹 Select Business Type (Radio Button)**
def select_radio_button(driver, radio_id):
    try:
        verify_element_exists(driver, By.ID, radio_id)  # Check if element exists
        radio_button = driver.find_element(By.ID, radio_id)
        driver.execute_script("arguments[0].click();", radio_button)  # JavaScript click
        print(f"✅ Radio button '{radio_id}' selected successfully!")
    except Exception as e:
        print(f"❌ Error selecting radio button: {e}")


# **🔹 Click Next Button**
def click_next_button(driver):
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))
        )
        next_button.click()
        print("✅ 'Next' button clicked successfully!")
    except Exception as e:
        print(f"❌ Error clicking 'Next' button: {e}")


# **🔹 Save User Data in CSV**
def save_user_to_csv(user_data):
    file_path = "registered_users.csv"
    file_exists = os.path.exists(file_path)

    fieldnames = [
        "full_name", "username", "email", "password", "date_of_birth",
        "address", "city", "state", "zip_code", "phone_number",
        "company", "job_title"
    ]

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # Write header only once

        writer.writerow(user_data)
        print(f"✅ User data saved: {user_data}")


# **🔹 Show Exit Dialog**
def show_exit_dialog():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Process Completed", "Signup process completed! Click OK to close the browser.")
    root.destroy()


# **🔹 Main Execution**
if __name__ == "__main__":
    driver = setup_driver()
    driver.get("https://www.pinterest.com")
    time.sleep(3)

    click_signup_button(driver)
    time.sleep(2)

    click_business_account_button(driver)
    time.sleep(2)

    while True:
        fake_user = generate_fake_user()  # Generate fake user data
        enter_email(driver, fake_user["email"])
        enter_password(driver, fake_user["password"])
        enter_birthdate(driver, fake_user["date_of_birth"])

        click_create_account_button(driver)
        time.sleep(3)  # Wait for validation response

        old_url = driver.current_url
        time.sleep(5)  # Allow page to change
        if old_url != driver.current_url:
            save_user_to_csv(fake_user)
            break
        else:
            print("❌ Retrying with new user data...")

    # **Go to Business Setup Page & Select Business Type**
    driver.get("https://www.pinterest.com/business/hub/")
    time.sleep(5)

    select_radio_button(driver, "publisher_or_media")  # Select "Publisher or Media"
    time.sleep(2)

    click_next_button(driver)
    time.sleep(2)

    show_exit_dialog()  # Show exit message
    driver.quit()
