import csv
import os

import tkinter as tk
import random
import re
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from src.utils.story_generator import generate_story
from utils.fake_data import generate_fake_user  # Import Fake Data Generator
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select



statusValue = None

# **🔹 Setup WebDriver**
def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver_ = webdriver.Chrome(service=service, options=options)
    return driver_


# **🔹 Click Signup Button**
# def click_signup_button(driver):
#     try:
#         signup_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//div[@data-test-id='simple-signup-button']//button"))
#         )
#         signup_button.click()
#         print("✅ Signup button clicked successfully!")
#     except Exception as e:
#         print(f"❌ Error clicking signup button: {e}")


def click_signup_button(driver_):

    global statusValue
    attempts = 2  # Maximum attempts
    while attempts > 0:
        try:
            signup_button = WebDriverWait(driver_, 10).until(
                ec.element_to_be_clickable((By.XPATH, "//div[@data-test-id='simple-signup-button']//button"))
            )
            signup_button.click()
            statusValue = "✅ Signup button clicked successfully!"
            print(statusValue)
            break  # Exit the loop if the click is successful
        except Exception as e:
            attempts -= 1  # Decrease attempts after a failure
            statusValue = f"❌ Error clicking signup button: {e}"
            print(statusValue)
            if attempts > 0:

                statusValue = "⏳ Retrying..."
                print(statusValue)
                time.sleep(2)  # Optional: sleep for a while before retrying
            else:
               statusValue = "❌ Failed to click signup button after retrying."
               print(statusValue)


# **🔹 Click Business Account Button**
def click_business_account_button(driver_):
    global statusValue
    """
    Clicks the 'Create a Free Business Account' button and retries up to 2 times if the click fails.
    """
    attempt = 0
    while attempt < 2:  # Try clicking up to 2 times
        try:
            # Wait for the button to be clickable
            business_account_button = WebDriverWait(driver_, 10).until(
                ec.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Create a free business account')]"))
            )

            try:
                business_account_button.click()  # Normal click
            except ElementClickInterceptedException:


                statusValue = f"🔄 Attempt {attempt+1}: Click intercepted, retrying with JavaScript..."
                print(statusValue)
                driver_.execute_script("arguments[0].click();", business_account_button)  # JS Click Fallback

            statusValue = f"✅ 'Create a Free Business Account' button clicked successfully on attempt {attempt+1}!"
            print(statusValue)
            return  # Exit the function after success

        except TimeoutException:

            statusValue = f"❌ Attempt {attempt+1}: 'Create a Free Business Account' button not found."
            print(statusValue)

        except Exception as e:

            statusValue = f"❌ Attempt {attempt+1}: Unexpected error: {e}"
            print(statusValue)

        attempt += 1  # Increase attempt count

    statusValue = "❌ Failed to click 'Create a Free Business Account' after 2 attempts."
    print(statusValue)



# **🔹 Clear & Enter Text**
def clear_and_enter_text(field, text):
    global  statusValue
    try:
        field.send_keys(Keys.CONTROL + "a")
        field.send_keys(Keys.DELETE)
        field.send_keys(text)
    except Exception as e:


        statusValue = f"❌ Error clearing and entering text: {e}"
        print(statusValue)


# **🔹 Enter Email**
def enter_email(driver_, email):
    global  statusValue
    try:
        email_field = WebDriverWait(driver_, 10).until(
            ec.presence_of_element_located((By.ID, "email"))
        )
        clear_and_enter_text(email_field, email)
        statusValue = f"✅ Email entered: {email}"
        print(statusValue)

    except Exception as e:
        statusValue = f"❌ Error entering email: {e}"
        print(statusValue)


# **🔹 Enter Password**
def enter_password(driver_, password):
    global statusValue
    try:
        password_field = WebDriverWait(driver_, 10).until(
            ec.presence_of_element_located((By.ID, "password"))
        )
        clear_and_enter_text(password_field, password)

        statusValue = f"✅ Password entered: {password}"
        print(statusValue)

    except Exception as e:

        statusValue =f"❌ Error entering password: {e}"
        print(statusValue)


# **🔹 Enter Birthdate**
def enter_birthdate(driver_, birthdate):
    global statusValue
    try:
        birthdate_field = WebDriverWait(driver_, 10).until(
            ec.presence_of_element_located((By.ID, "birthdate"))
        )
        clear_and_enter_text(birthdate_field, birthdate)

        statusValue = f"✅ Birthdate entered: {birthdate}"
        print(statusValue)

    except Exception as e:

        statusValue = f"❌ Error entering birthdate: {e}"
        print(statusValue)


# **🔹 Click 'Create Account' Button**
def click_create_account_button(driver_):
    global statusValue
    try:
        create_account_button = WebDriverWait(driver_, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(., 'Create account')]"))
        )
        create_account_button.click()

        statusValue ="✅ 'Create account' button clicked successfully!"
        print(statusValue)

    except Exception as e:

        statusValue = f"❌ Error clicking 'Create account' button: {e}"

        print(statusValue)


# **🔹 Save User Data in CSV**
def save_user_to_csv(user_data):
    global statusValue
    file_path = "registered_users.csv"
    file_exists = os.path.exists(file_path)

    fieldnames = [
        "full_name", "gender","username", "email", "password", "date_of_birth",
        "address", "city", "state", "zip_code", "phone_number",
        "company", "job_title"
    ]

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # Write header only once

        writer.writerow(user_data)


        statusValue =f"✅ User data saved: {user_data}"
        print(statusValue)



# **🔹 Select Business Type (Radio Button)**
def select_radio_button(driver_, radio_id):
    global statusValue
    try:
        radio_button = WebDriverWait(driver_, 10).until(
            ec.presence_of_element_located((By.ID, radio_id))
        )
        driver_.execute_script("arguments[0].click();", radio_button)  # JavaScript click
        statusValue = f"✅ Radio button '{radio_id}' selected successfully!"
        print(statusValue)

    except Exception as e:
        statusValue = f"❌ Error selecting radio button: {e}"
        print(statusValue)


# **🔹 Click Next Button**
def click_next_button(driver_):
    global statusValue
    try:
        next_button = WebDriverWait(driver_, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))
        )
        next_button.click()

        statusValue = "✅ 'Next' button clicked successfully!"
        print(statusValue)

    except Exception as e:


        statusValue = f"❌ Error clicking 'Next' button: {e}"
        print(statusValue)


# **🔹 Enter Business Name**
def enter_business_name(driver_, business_name):

    global  statusValue
    try:
        business_name_field = WebDriverWait(driver_, 10).until(
            ec.presence_of_element_located((By.ID, "businessName"))
        )
        clear_and_enter_text(business_name_field, business_name.upper())  # Capitalize username
        statusValue = f"✅ Business name entered: {business_name.upper()}"

        print(statusValue)
    except Exception as e:

        statusValue = f"❌ Error entering business name: {e}"
        print(statusValue)


# **🔹 Select 'No Website' Checkbox**
def select_no_website_checkbox(driver_):
    global statusValue
    try:
        no_website_checkbox = WebDriverWait(driver_, 10).until(
            ec.presence_of_element_located((By.ID, "noWebsite"))
        )
        driver_.execute_script("arguments[0].click();", no_website_checkbox)  # JavaScript Click
        statusValue = "✅ 'No Website' checkbox selected successfully!"
        print(statusValue)
    except Exception as e:
        print(f"❌ Error selecting 'No Website' checkbox: {e}")


# **🔹 Select Goal from Dropdown**
def select_goal(driver_, goal_text="Create content on Pinterest to grow an audience"):

    global statusValue
    try:
        # Wait for the dropdown input to be clickable
        goal_input = WebDriverWait(driver_, 10).until(
            ec.element_to_be_clickable((By.ID, "combobox-tags"))
        )
        goal_input.click()  # Click to activate dropdown
        time.sleep(2)  # Allow dropdown to appear

        # Enter the text
        goal_input.send_keys(goal_text)
        time.sleep(2)  # Allow suggestions to load

        # Press ARROW_DOWN 3 times to move to the 4th option
        for _ in range(4):
            goal_input.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)  # Small delay to allow dropdown navigation

        # Press Enter to select the highlighted option
        goal_input.send_keys(Keys.ENTER)

        statusValue =  f"✅ 4th Goal selected: {goal_text}"

        print(statusValue)

    except Exception as e:

        statusValue =  f"❌ Error selecting goal: {e}"

        print(statusValue)


niche_value = None

# **🔹 Select Business Category (Beauty or Fashion)**
def select_business_category(driver_):
    global statusValue
    try:
        global niche_value
        category_dropdown = WebDriverWait(driver_, 10).until(
            ec.presence_of_element_located((By.ID, "verticals"))
        )
        business_categories = ["BEAUTY", "FASHION"]
        selected_category = random.choice(business_categories)  # Randomly select one

        niche_value = selected_category

        category_dropdown.click()
        time.sleep(1)

        option_xpath = f"//select[@id='verticals']/option[@value='{selected_category}']"
        option = WebDriverWait(driver_, 5).until(
            ec.element_to_be_clickable((By.XPATH, option_xpath))
        )
        option.click()

        statusValue = f"✅ Selected business category: {selected_category}"
        print(statusValue)

    except Exception as e:
        statusValue =  f"❌ Error selecting business category: {e}"
        print(statusValue)


# **🔹 Click 'Done' Button**
def click_done_button(driver_):
    global statusValue
    try:
        done_button = WebDriverWait(driver_, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'B1n tg7 tBJ dyH iFc sAJ H2s') and text()='Done']"))
        )
        done_button.click()


        statusValue =  "✅ 'Done' button clicked successfully!"
        print(statusValue)

    except Exception as e:

        statusValue =  f"❌ Error clicking 'Done' button: {e}"
        print(statusValue)


    # **🔹 Click 'Build Your Profile' Button**
def click_correct_build_profile(driver_):
    try:
        profile_button = WebDriverWait(driver_, 10).until(
            ec.element_to_be_clickable(
                (By.XPATH, "//div[@role='button' and @aria-label='Build your profile'][descendant::h2[contains(text(), 'Showcase your brand')]]")
            )
        )
        profile_button.click()
        print("✅ 'Build Your Profile' button clicked successfully!")
    except Exception as e:
        print(f"❌ Error clicking 'Build Your Profile' button: {e}")


# **🔹 Click 'Next' Button (After 'Build Your Profile')**
def click_next_after_build_profile(driver_):
    try:
        next_button = WebDriverWait(driver_, 10).until(
            ec.element_to_be_clickable(
                (By.XPATH, "//a[contains(@class, 'S9z') and contains(@href, '/settings')]//div[text()='Next']"))
        )
        next_button.click()
        print("✅ 'Next' button clicked successfully!")
    except Exception as e:
        print(f"❌ Error clicking 'Next' button: {e}")


#--------------------------------------------------------------------------------------------------------------

def select_pronoun(driver_, gender_):
    """
    Selects the correct pronoun in the input field based on gender.

    :param driver_: Selenium WebDriver instance
    :param gender_: String value, "male" selects "he/him", "female" selects "she/her"
    """
    try:
        wait = WebDriverWait(driver_, 5)

        # Find the pronoun input field
        pronoun_input = wait.until(ec.presence_of_element_located((By.ID, "combobox-pronouns")))

        # Determine the correct pronoun
        pronoun_to_select = "he/him" if gender_.lower() == "male" else "she/her"

        # Click the input field to activate it
        pronoun_input.click()
        time.sleep(1)

        # Clear the input field and send the pronoun
        pronoun_input.clear()
        pronoun_input.send_keys(pronoun_to_select)
        time.sleep(1)

        # Confirm selection by sending ENTER
        pronoun_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Allow UI to update

        # Use JavaScript to ensure value is properly set in the DOM
        driver_.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", pronoun_input)
        time.sleep(1)

        # Click anywhere outside the input box to confirm the selection
        driver_.find_element(By.TAG_NAME, "body").click()
        time.sleep(1)

        print(f"✅ Pronoun '{pronoun_to_select}' selected successfully!")

    except Exception as e:
        print(f"❌ Error selecting pronoun: {str(e)}")

#
# def generate_story(name, city, address, state, niche):
#     """
#     Generate a personalized bio/story for a content creator in the 'fashion' or 'beauty' niche.
#     """
#     # Story templates based on the niche
#     story_templates = {
#         "fashion": [
#             f"Hey there! I’m {name}, a fashion enthusiast from {city}, {state}. 👗✨ "
#             f"Growing up in {address}, I fell in love with styling and trends. "
#             f"My content is all about helping you express yourself through fashion and confidence!",
#
#             f"Hi, I’m {name} from {city}, {state}, your go-to fashion stylist! 💃🕶️ "
#             f"I started experimenting with outfits in my home at {address}, and now I inspire others "
#             f"to embrace their unique style with the latest fashion trends!"
#         ],
#         "beauty": [
#             f"Hello, gorgeous! I’m {name}, a beauty creator from {city}, {state}. 💄🌟 "
#             f"Living in {address} taught me the magic of skincare and makeup. "
#             f"My goal? To help you glow inside and out with tips, tricks, and reviews!",
#
#             f"Hi, I’m {name}, a makeup lover from {city}, {state}! 💅✨ "
#             f"From my first beauty experiments at {address} to mastering glam looks, "
#             f"I share everything about skincare, makeup hacks, and beauty essentials!"
#         ]
#     }
#
#     # Select a story template based on the niche
#     return random.choice(story_templates.get(niche, story_templates["fashion"]))  # Default to "fashion"
#--------------------------------------------------------------------------------------------------------------


# **🔹 Fill Settings Form**
# def fill_settings_form(driver, address, city, region, country):
#     try:
#         # Find the input field for the address
#         address_field = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "partner_address_line_1"))
#         )
#         clear_and_enter_text(address_field, address)  # Enter the address
#         print(f"✅ Address entered: {address}")
#
#         # Find and fill other fields (city, region, country)
#         city_field = driver.find_element(By.ID, "partner_city")
#         clear_and_enter_text(city_field, city)
#         print(f"✅ City entered: {city}")
#
#         region_field = driver.find_element(By.ID, "partner_region")
#         clear_and_enter_text(region_field, region)
#         print(f"✅ Region entered: {region}")
#
#         country_field = driver.find_element(By.ID, "partner_country")
#         clear_and_enter_text(country_field, country)
#         print(f"✅ Country entered: {country}")
#
#     except Exception as e:
#         print(f"❌ Error filling settings form: {e}")

# def fill_settings_form(driver, address, city, region, country):
#     try:
#         # Address Field
#         address_field = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "partner_address_line_1"))
#         )
#         address_field.click()
#         address_field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)  # Clear field
#         address_field.send_keys(address)
#         print(f"✅ Address entered: {address}")
#
#         # City Field
#         city_field = driver.find_element(By.ID, "partner_city")
#         city_field.click()
#         city_field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)  # Clear field
#         city_field.send_keys(city)
#         print(f"✅ City entered: {city}")
#
#         # Region Field
#         region_field = driver.find_element(By.ID, "partner_region")
#         region_field.click()
#         region_field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)  # Clear field
#         region_field.send_keys(region)
#         print(f"✅ Region entered: {region}")
#
#         # Country Field (Dropdown Selection)
#         country_dropdown = Select(driver.find_element(By.ID, "partner_country"))
#         country_dropdown.select_by_visible_text(country)  # Select by visible text
#         print(f"✅ Country selected: {country}")
#
#         # Click outside to remove focus
#         driver.find_element(By.TAG_NAME, "body").click()
#
#     except Exception as e:
#         print(f"❌ Error filling settings form: {e}")

def remove_non_bmp(text):
    """Removes characters outside the BMP (Basic Multilingual Plane)"""
    return re.sub(r'[^\u0000-\uFFFF]', '', text)

def fill_story_field(driver_, story_):
    """Fills the 'Tell your story' field with cleaned text"""
    try:
        # Initialize WebDriverWait and ActionChains
        wait = WebDriverWait(driver_, 10)
        actions = ActionChains(driver_)

        # Clean the input story
        cleaned_story = remove_non_bmp(story_)

        # Locate the story input field
        story_field = wait.until(ec.presence_of_element_located((By.ID, "about")))

        # Scroll into view and click the field
        driver_.execute_script("arguments[0].scrollIntoView();", story_field)
        actions.move_to_element(story_field).click().perform()

        # Clear the existing text
        story_field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)

        # Enter the cleaned text
        story_field.send_keys(cleaned_story)

        print(f"✅ Story entered successfully: {cleaned_story}")

    except Exception as e:
        print(f"❌ Error filling 'Tell your story' field: {e}")



def fill_settings_form(driver_, address, city_, region): #country
    try:

#----------------------------------------------------------
        # wait = WebDriverWait(driver, 10)
        # actions = ActionChains(driver)

        # # "Tell your story" Field
        # story_field = wait.until(EC.presence_of_element_located((By.ID, "about")))
        # driver.execute_script("arguments[0].scrollIntoView();", story_field)
        # actions.move_to_element(story_field).click().perform()
        # story_field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)  # Clear field
        # story_field.send_keys(story)
        # print(f"✅ Story entered: {story}")

#-----------------------------------------------------

        # Address Field
        address_field = WebDriverWait(driver_, 10).until(
            ec.presence_of_element_located((By.ID, "partner_address_line_1"))
        )

        driver_.execute_script("arguments[0].scrollIntoView();", address_field)  # Scroll into view
        ActionChains(driver_).move_to_element(address_field).click().perform()  # Click using Actions
        address_field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)  # Clear field
        address_field.send_keys(address)
        print(f"✅ Address entered: {address}")

        # City Field
        city_field = driver_.find_element(By.ID, "partner_city")
        driver_.execute_script("arguments[0].scrollIntoView();", city_field)
        city_field.click()
        city_field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        city_field.send_keys(city_)
        print(f"✅ City entered: {city_}")

        # Region Field
        region_field = driver_.find_element(By.ID, "partner_region")
        driver_.execute_script("arguments[0].scrollIntoView();", region_field)
        region_field.click()
        region_field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        region_field.send_keys(region)
        print(f"✅ Region entered: {region}")

        # Country Field (Dropdown Selection)
        # country_dropdown = Select(driver.find_element(By.ID, "partner_country"))
        # driver.execute_script("arguments[0].scrollIntoView();", country_dropdown)
        # country_dropdown.select_by_visible_text(country)
        # print(f"✅ Country selected: {country}")



        # Click outside to remove focus
        driver_.find_element(By.TAG_NAME, "body").click()

    except Exception as e:
        print(f"❌ Error filling settings form: {e}")


def select_country(driver_, country):
    """Selects a country from the dropdown menu."""
    try:
        # Find the dropdown element
        country_dropdown_element = driver_.find_element(By.ID, "partner_country")

        # Scroll into view properly
        driver_.execute_script("arguments[0].scrollIntoView();", country_dropdown_element)

        # Initialize Select with the element
        country_dropdown = Select(country_dropdown_element)

        # Select the desired country
        country_dropdown.select_by_visible_text(country)

        print(f"✅ Country selected: {country}")

    except Exception as e:
        print(f"❌ Error selecting country: {e}")


def click_save_button_setting_page(driver_):
    try:
        # Wait until the button becomes enabled (i.e., no 'disabled' attribute)
        save_button_ = WebDriverWait(driver_, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//button[.//div[text()='Save']]"))
        )

        # Click the button
        save_button_.click()
        print("✅ 'Save' button clicked successfully!")

    except Exception as e:
        print(f"❌ Error clicking 'Save' button: {e}")

def go_to_account_management_page(driver_):
    try:
        # Wait for the element to be present
        account_management_element = WebDriverWait(driver_, 10).until(
            ec.presence_of_element_located((By.XPATH, "//div[text()='Account management']"))
        )

        # Scroll the element into view to avoid any overlays
        driver_.execute_script("arguments[0].scrollIntoView(true);", account_management_element)
        time.sleep(1)  # Wait briefly for scrolling to complete

        # Attempt to click using JavaScript as a fallback
        try:
            account_management_element.click()
            print("✅ Navigated to Account Management page.")
        except Exception:
            print("⚠️ Direct click failed, trying JavaScript click...")
            driver_.execute_script("arguments[0].click();", account_management_element)
            print("✅ Navigated to Account Management page using JavaScript.")

    except Exception as e:
        print(f"❌ Error navigating to Account Management page: {e}")


# **🔹 Function to Select Gender**
# def select_gender(driver, gender_value):
#     try:
#         # Wait until the radio buttons are visible
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.NAME, "gender"))
#         )
#
#         # Define a dictionary to map gender values to radio button ids
#         gender_options = {
#             "male": "male",
#             "female": "female",
#             "unspecified": "unspecified"
#         }
#
#         # Check if the provided gender_value is valid and find the corresponding radio button
#         if gender_value.lower() in gender_options:
#             gender_id = gender_options[gender_value.lower()]
#
#             # Find the radio button by ID and click it
#             gender_radio_button = driver.find_element(By.ID, gender_id)
#             gender_radio_button.click()
#
#             print(f"✅ Gender selected: {gender_value}")
#         else:
#             print("❌ Invalid gender value. Please choose from 'male', 'female', or 'unspecified'.")
#
#     except Exception as e:
#         print(f"❌ Error selecting gender: {e}")


#--------------------------------------------------------------------------------------------------

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
# import time


def select_gender(driver_, gender_value):
    """
    Selects a gender radio button based on the provided gender value.

    Ensures the selection is successful before proceeding.

    :param driver_: Selenium WebDriver instance
    :param gender_value: The gender to select ('male', 'female', or 'unspecified')
    """
    try:
        # Wait until the page loads fully
        WebDriverWait(driver_, 10).until(ec.presence_of_element_located((By.NAME, "gender")))

        # Mapping gender values to labels
        gender_labels = {
            "male": "male",
            "female": "female",
            "unspecified": "unspecified"
        }

        # Validate gender input
        gender_value = gender_value.lower()
        if gender_value not in gender_labels:
            print("❌ Invalid gender value! Choose from 'male', 'female', or 'unspecified'.")
            return False

        # Gender label XPath
        gender_xpath = f"//label[@for='{gender_labels[gender_value]}']"

        # Ensure the element is visible on screen
        gender_label = WebDriverWait(driver_, 10).until(
            ec.presence_of_element_located((By.XPATH, gender_xpath))
        )
        driver_.execute_script("arguments[0].scrollIntoView({block: 'center'});", gender_label)

        # Try multiple times if clicking is blocked
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                # Ensure the element is clickable
                WebDriverWait(driver_, 5).until(ec.element_to_be_clickable((By.XPATH, gender_xpath)))

                # Click using JavaScript to bypass overlays
                driver_.execute_script("arguments[0].click();", gender_label)

                # Confirm selection (wait for input to be selected)
                selected = WebDriverWait(driver_, 3).until(
                    ec.element_located_to_be_selected((By.ID, gender_labels[gender_value]))
                )

                if selected:
                    print(f"✅ Gender successfully selected: {gender_value.capitalize()}")
                    return True  # Success

            except Exception:
                print(f"⚠️ Attempt {attempt + 1}: Click failed, retrying...")
                time.sleep(1)  # Small delay before retrying

        print("❌ Failed to select gender after multiple attempts!")
        return False  # Failure

    except Exception as e:
        print(f"❌ Error selecting gender: {e}")
        return False




#------------------------------------------------------------
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

def select_random_checkboxes_excluding_not_sure(driver_, max_attempts=3):

    global statusValue
    """
    Selects exactly 3 random checkboxes excluding 'Not sure yet' option.
    Retries up to max_attempts if checkboxes are not found or clickable.
    """
    attempt = 1

    while attempt <= max_attempts:
        try:
            wait = WebDriverWait(driver_, 10)

            # ✅ Locate all checkboxes excluding 'Not sure yet'
            checkboxes = wait.until(
                ec.presence_of_all_elements_located(
                    (By.XPATH, "//input[@type='checkbox' and not(@id='not_sure')]")
                )
            )

            # ✅ Ensure there are at least 3 checkboxes available
            if len(checkboxes) < 3:
                print(f"⚠️ Attempt {attempt}: Less than 3 valid checkboxes found. Retrying...")
                driver_.execute_script("window.scrollBy(0, 200);")  # Scroll slightly
                time.sleep(2)
                attempt += 1
                continue

            # ✅ Select exactly 3 random checkboxes
            random_checkboxes = random.sample(checkboxes, 3)

            for checkbox in random_checkboxes:
                try:
                    driver_.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                    time.sleep(0.5)  # Stability delay

                    # ✅ Check if checkbox is not already selected
                    if not checkbox.is_selected():
                        wait.until(ec.element_to_be_clickable(checkbox)).click()
                        time.sleep(1)  # Small delay for UI stability
                    else:
                        print(f"ℹ️ Checkbox already selected: {checkbox.get_attribute('id')}")

                except ElementClickInterceptedException:
                    print(f"⚠️ Retrying click for {checkbox.get_attribute('id')} via JavaScript")
                    driver_.execute_script("arguments[0].click();")

            selected_ids = [cb.get_attribute('id') for cb in random_checkboxes]
            print(f"✅ Selected checkboxes: {selected_ids}")
            return True

        except TimeoutException:
            print(f"❌ Timeout on attempt {attempt}. Retrying...")

            driver_.execute_script("window.scrollBy(0, -200);")  # Scroll up & retry
            time.sleep(2)
            attempt += 1

    statusValue ="❌ Max retry attempts reached. Checkboxes not found."
    print(statusValue)
    return False



def click_save_button_acc_management(driver_):
    global statusValue
    try:
        wait = WebDriverWait(driver_, 10)

        # Locate the Save button
        save_button_ = wait.until(
            ec.presence_of_element_located((By.XPATH, "//button[contains(@class, 'RCK') and div/div[text()='Save']]"))
        )

        # Scroll into view
        driver_.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button_)

        # Click the button
        save_button_.click()

        statusValue = "✅ Save button clicked successfully!"
        print(statusValue)

    except Exception as e:

        statusValue = f"❌ Error clicking Save button: {str(e)}"
        print(statusValue)




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

    address1 = None
    city = None
    state = None
    gender = None
    story = None
    name = None

    while True:
        fake_user = generate_fake_user()  # Generate fake user data
        enter_email(driver, fake_user["email"])
        enter_password(driver, fake_user["password"])
        enter_birthdate(driver, fake_user["date_of_birth"])

        city = fake_user["city"]
        address1 = fake_user["address"]
        state = fake_user["state"]
        gender = fake_user["gender"]
        name = fake_user['full_name']


        click_create_account_button(driver)
        time.sleep(3)  # Wait for validation response

        old_url = driver.current_url
        time.sleep(5)  # Allow page to change
        if old_url != driver.current_url:
            save_user_to_csv(fake_user)
            break
        else:
            print("❌ Retrying with new user data...")

    driver.get("https://www.pinterest.com/business/hub/")
    time.sleep(5)

    select_radio_button(driver, "publisher_or_media")  # Select "Publisher or Media"
    time.sleep(2)

    click_next_button(driver)
    time.sleep(2)

    enter_business_name(driver, fake_user["username"])
    time.sleep(2)

    select_no_website_checkbox(driver)  # ✅ 'No Website' checkbox selected
    time.sleep(2)

    click_next_button(driver)  # ✅ Next button click after checkbox
    time.sleep(2)

    select_goal(driver)  # ✅ Select goal from dropdown
    time.sleep(2)

    select_business_category(driver)  # ✅ Business Category Selected
    time.sleep(2)

    click_done_button(driver)  # ✅ Click 'Done' button
    time.sleep(2)

    click_correct_build_profile(driver)  # ✅ Click correct 'Build Your Profile' button
    time.sleep(3)
    click_next_after_build_profile(driver)  # ✅ Click 'Next' button after profile step
    time.sleep(3)

    story = generate_story(name, city, state, gender, niche_value)
    time.sleep(2)

    fill_story_field(driver,story)
    time.sleep(2)

    select_pronoun(driver, gender)
    time.sleep(2)

    #print(story)
    fill_settings_form(driver,address1, city ,state)
    time.sleep(3)

    select_country(driver,"United States")
    time.sleep(3)


    click_save_button_setting_page(driver)
    time.sleep(3)

    # Navigate to the Account Management page
    go_to_account_management_page(driver)

    time.sleep(2)

    select_gender(driver, gender)
    time.sleep(2)

    #select_random_checkboxes_excluding_not_sure(driver)
    #time.sleep(5)


    # click_save_button_acc_management(driver)
    # time.sleep(2)

    if select_random_checkboxes_excluding_not_sure(driver):
        print("✅ Checkboxes selected successfully.")
    else:
        print("❌ Form not submitted. Checkboxes selection failed.")

    click_save_button_acc_management(driver)
    time.sleep(2)

    #show_exit_dialog()
    driver.quit()
