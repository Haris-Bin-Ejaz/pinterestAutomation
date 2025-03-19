import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import subprocess
import sys
import psutil
import pandas as pd
import os

running = False
current_cycle = 0
total_cycles = 0
process = None

# Define paths
MAIN_SCRIPT_PATH = r"D:\My Projects\Automation\pinterest-automation\src\main.py"
CSV_FILE_PATH = r"D:\My Projects\Automation\pinterest-automation\src\registered_users.csv"
XLSX_FILE_PATH = r"D:\My Projects\Automation\pinterest-automation\src\emails_passwords.xlsx"


def update_status():
    status_label.config(text=f"Cycle: {current_cycle}/{total_cycles}")


def start_script():
    global running, current_cycle, total_cycles, process

    if running:
        return
    running = True
    current_cycle = 0
    total_cycles = int(repeat_entry.get())

    def run():
        global running, current_cycle
        venv_python = sys.executable

        for i in range(total_cycles):
            if not running:
                break
            current_cycle = i + 1
            update_status()

            try:
                process = subprocess.Popen([venv_python, MAIN_SCRIPT_PATH])
                process.wait()
            except Exception as e:
                status_label.config(text=f"Error: {e}")

            time.sleep(1)

        running = False
        status_label.config(text="Finished ✅")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()


def stop_script():
    global running
    running = False
    messagebox.showinfo("Stopping", "Process will stop after completing the current cycle.")


def force_stop_script():
    global running, process
    running = False

    if process and process.poll() is None:
        try:
            parent = psutil.Process(process.pid)
            for child in parent.children(recursive=True):
                child.terminate()
            parent.terminate()
            status_label.config(text="Force Stopped ⛔")
            messagebox.showwarning("Force Stopped", "Process was terminated immediately.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to force stop: {e}")
    else:
        messagebox.showinfo("Info", "No active process to stop.")


def extract_email_password():
    """Extracts email & password from `registered_users.csv` and saves to `emails_passwords.xlsx`."""
    try:
        df = pd.read_csv(CSV_FILE_PATH, header=None)

        # Expected column indexes (Based on given format)
        email_col = 3  # 4th column (Indexing starts from 0)
        password_col = 4  # 5th column

        # Extract Email & Password columns
        df_selected = df.iloc[:, [email_col, password_col]]

        # Rename columns for clarity
        df_selected.columns = ["Email", "Password"]

        # Save as Excel file
        df_selected.to_excel(XLSX_FILE_PATH, index=False, engine="openpyxl")

        messagebox.showinfo("Success", f"✅ Email & Passwords saved successfully:\n{XLSX_FILE_PATH}")

        # Open folder containing the extracted file
        os.startfile(os.path.dirname(XLSX_FILE_PATH))

    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to extract data: {e}")


def start_gui():
    global root, status_label, repeat_entry
    root = tk.Tk()
    root.title("Pinterest Automation")
    root.geometry("450x400")
    root.configure(bg="white")

    frame = tk.Frame(root, bg="white", bd=2, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=300)

    tk.Label(frame, text="Pinterest Automation", font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=10)

    tk.Label(frame, text="Number of Repeats:", bg="white", font=("Arial", 10)).pack()
    repeat_entry = ttk.Entry(frame, font=("Arial", 10))
    repeat_entry.pack(pady=5)
    repeat_entry.insert(0, "1")

    ttk.Button(frame, text="Start", command=start_script).pack(pady=5)
    ttk.Button(frame, text="Stop", command=stop_script).pack(pady=5)
    ttk.Button(frame, text="Force Stop", command=force_stop_script).pack(pady=5)

    # New Button to Extract & Open File
    ttk.Button(frame, text="Extract & Open File", command=extract_email_password).pack(pady=5)

    status_label = tk.Label(frame, text="Status: Waiting...", bg="white", font=("Arial", 10), fg="gray")
    status_label.pack(pady=10)

    root.mainloop()


# Prevent auto-run if imported
if __name__ == "__main__":
    start_gui()
