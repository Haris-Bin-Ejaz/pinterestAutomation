from faker import Faker
import random
import string
import re

# Initialize Faker with US locale
fake = Faker("en_US")

# Global counter for sequential password uniqueness
password_counter = 1000  # Start from 1000 to maintain resemblance


# Function to generate a sequential secure password with a prefix
def generate_password():
    global password_counter
    prefix = "PTAC"  # Fixed prefix for resemblance

    base_number = str(password_counter)[-2:]  # Last 2 digits of counter
    special_chars = "!@#$%^&*"  # Allowed special characters
    upper_char = random.choice(string.ascii_uppercase)  # At least one uppercase
    lower_char = random.choice(string.ascii_lowercase)  # At least one lowercase
    special_char = random.choice(special_chars)  # At least one special character

    password_counter += 1  # Increment counter for uniqueness

    # Assemble password: "PTAC" + Random Mix (Ensuring all requirements)
    password = f"{prefix}{special_char}{upper_char}{lower_char}{base_number}"

    return password[:10]  # Ensure max length is 10 characters


# Function to generate a birthdate between 1992 and 1996
def generate_birthdate():
    year = random.randint(1992, 1996)  # Restrict year between 1992-1996
    month = random.randint(1, 12)  # Random month
    day = random.randint(1, 28)  # Random day (safe for all months)

    return f"{month:02d}/{day:02d}/{year}"  # Format: MM/DD/YYYY


# Function to generate a realistic email and username
def generate_fake_user():
    # Randomly choose gender for name generation
    gender = random.choice(["male", "female"])  # Randomly assign gender
    if gender == "male":
        first_name = fake.first_name_male()
    else:
        first_name = fake.first_name_female()

    last_name = fake.last_name()

    # Generate a username without spaces or special characters
    username = re.sub(r'\W+', '', f"{first_name.lower()}{last_name.lower()}")

    # Choose a more realistic email format
    email_formats = [
        f"{first_name[0].lower()}{last_name.lower()}@outlook.com",
        f"{first_name.lower()}{last_name.lower()}{random.randint(10, 99)}@gmail.com",
        f"{first_name.lower()}{last_name.lower()}{random.randint(10, 99)}@outlook.com"
    ]
    email = random.choice(email_formats)  # Select one realistic format

    # **US-based address data**
    address = fake.street_address()  # Random US street address
    city = fake.city()  # Random city in the US
    state = fake.state_abbr()  # US state abbreviation (e.g., CA, TX)
    zip_code = fake.zipcode()  # US zipcode

    # **🎯 Maintain the Same Return Structure**
    return {
        "full_name": f"{first_name} {last_name}",  # Full name is consistent
        "gender": gender,  # New gender field
        "username": username,  # Clean username
        "email": email,  # More realistic email
        "password": generate_password(),  # Uses sequential password generator
        "date_of_birth": generate_birthdate(),  # ✅ Restricted to 1992-1996
        "address": address,  # US-based address
        "city": city,  # US-based city
        "state": state,  # US-based state abbreviation
        "zip_code": zip_code,  # US-based zip code
        "phone_number": fake.phone_number(),
        "company": fake.company(),
        "job_title": fake.job()
    }


# **✅ Run this script to test if everything is working properly**
if __name__ == "__main__":
    for _ in range(5):  # Generate 5 users to test uniqueness
        print(generate_fake_user())
