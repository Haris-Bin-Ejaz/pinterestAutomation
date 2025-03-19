import pandas as pd

# Define file paths (Update if needed)
csv_file_path = "D:/My Projects/Automation/pinterest-automation/src/registered_users.csv"
xlsx_file_path = "D:/My Projects/Automation/pinterest-automation/src/emails_passwords.xlsx"  # ✅ Use .xlsx

def extract_email_password():
    try:
        # Load CSV without headers
        df = pd.read_csv(csv_file_path, header=None)

        # Define expected column indexes (Based on given format)
        email_col = 3  # 4th column (Indexing starts from 0)
        password_col = 4  # 5th column

        # Extract only Email & Password columns
        df_selected = df.iloc[:, [email_col, password_col]]

        # Rename columns for clarity
        df_selected.columns = ["Email", "Password"]

        # Save as Excel file (.xlsx) using openpyxl
        df_selected.to_excel(xlsx_file_path, index=False, engine="openpyxl")

        print(f"✅ Email & Passwords saved successfully: {xlsx_file_path}")

    except Exception as e:
        print(f"❌ Error processing file: {e}")

# Run the function
extract_email_password()
