import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import time
from chipin_data import add_user
from tkcalendar import Calendar
import datetime
import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Helper functions
def connect_db():
    return sqlite3.connect("chipin.db")

def authenticate_user(username, password, table="users"):
    with connect_db() as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table} WHERE username=? AND password=?" if table == "users" else f"SELECT * FROM {table} WHERE admin_id=? AND password=?"
        cursor.execute(query, (username, password))
        return cursor.fetchone() is not None

def show_main_page():
    clear_screen()
    root.title("Main Page")
    tk.Label(root, text="Welcome to the Main Page!", font=("Arial", 18)).pack(pady=20)
    show_service_selection()  # Call the service selection function

#new1
def show_service_selection():
    clear_screen()
    root.title("Choose Your Service")

    tk.Label(root, text="Select a Service", font=("Arial", 18)).pack(pady=20)

    # Fetch services from the database
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT NAME FROM SERVICES")
        services = [row[0] for row in cursor.fetchall()]

    # Default selection
    selected_service = tk.StringVar(value=services[0])

    # Dropdown menu
    service_menu = ttk.OptionMenu(root, selected_service, services[0], *services)
    service_menu.pack(pady=10)

    def confirm_service():
        service = selected_service.get()
        show_scheduling_page(service)  # Go to next step with selected service

    tk.Button(root, text="Confirm Selection", command=confirm_service).pack(pady=20)
    tk.Button(root, text="Back", command=show_home_screen).pack(pady=10)
#new 2
# Global calendar service
calendar_service = None

def authenticate_google_calendar():
    global calendar_service
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    calendar_service = build('calendar', 'v3', credentials=creds)

def show_scheduling_page(service_name):
    clear_screen()
    root.title("Schedule Appointment")

    tk.Label(root, text=f"Schedule for {service_name}", font=("Arial", 18)).pack(pady=10)

    # Date selector
    tk.Label(root, text="Pick a Date:").pack()
    calendar = Calendar(root, selectmode='day')
    calendar.pack(pady=10)

    # Time selector
    tk.Label(root, text="Pick a Start Time (24H):").pack()
    times = [f"{h:02}:00" for h in range(8, 18)]  # 8 AM to 5 PM
    time_var = tk.StringVar(value=times[0])
    tk.OptionMenu(root, time_var, *times).pack(pady=10)

    def check_availability():
        date = calendar.get_date()
        time_str = time_var.get()
        start_datetime = datetime.datetime.strptime(f"{date} {time_str}", "%m/%d/%y %H:%M")
        end_datetime = start_datetime + datetime.timedelta(hours=4)

        # Check Google Calendar for conflicts
        events_result = calendar_service.events().list(
            calendarId="f5ff5981ab8fef089d2f43de1e5d1589dece29cd1d82922b5a260c8b86d67c78@group.calendar.google.com",
            timeMin=start_datetime.isoformat() + 'Z',
            timeMax=end_datetime.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if events:
            messagebox.showerror("Conflict", "Selected time overlaps with another event.")
        else:
            show_confirmation_page(service_name, start_datetime, end_datetime)

    tk.Button(root, text="Confirm Time", command=check_availability).pack(pady=20)
    tk.Button(root, text="Back", command=show_service_selection).pack(pady=10)
#new 3
def show_confirmation_page(service_name, start_time, end_time):
    clear_screen()
    root.title("Appointment Confirmed")

    tk.Label(root, text="Confirmation", font=("Arial", 18)).pack(pady=20)
    tk.Label(root, text=f"Service: {service_name}").pack()
    tk.Label(root, text=f"Start: {start_time.strftime('%A, %B %d %Y %H:%M')}").pack()
    tk.Label(root, text=f"End: {end_time.strftime('%H:%M')}").pack()

    tk.Button(root, text="Back to Home", command=show_home_screen).pack(pady=20)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

#not new

def show_loading_screen():
    clear_screen()
    root.title("Loading...")
    tk.Label(root, text="Loading, please wait...", font=("Arial", 16)).pack(pady=50)
    root.update()
    time.sleep(2)
    show_main_page()

def login_screen(title, is_admin=False):
    clear_screen()
    root.title(title)

    tk.Label(root, text=title, font=("Arial", 18)).pack(pady=20)
    tk.Label(root, text="Username:").pack(pady=(10, 5))
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:").pack(pady=(10, 5))
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    attempts_left = 3

    def handle_login():
        nonlocal attempts_left
        username = username_entry.get()
        password = password_entry.get()
        table = "admins" if is_admin else "users"

        if authenticate_user(username, password, table):
            messagebox.showinfo("Login Successful", "Welcome!")
            show_loading_screen()
        else:
            attempts_left -= 1
            if attempts_left > 0:
                messagebox.showerror("Login Failed", f"Wrong password. Try again ({attempts_left} attempts left).")
            else:
                messagebox.showerror("Login Failed", "Too many attempts. Returning to home screen.")
                show_home_screen()

    tk.Button(root, text="Log In", command=handle_login).pack(pady=20)
    tk.Button(root, text="Back to Home", command=show_home_screen).pack(pady=10)

def show_signup_screen():
    clear_screen()
    root.title("Sign Up Page")

    tk.Label(root, text="Sign Up", font=("Arial", 18)).pack(pady=20)
    tk.Label(root, text="Username:").pack(pady=(10, 5))
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:").pack(pady=(10, 5))
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    def handle_signup():
        username = username_entry.get()
        password = password_entry.get()
        if add_user(username, password):
            messagebox.showinfo("Sign Up Successful", "You can now log in!")
            show_home_screen()
        else:
            messagebox.showerror("Sign Up Failed", "Username already exists. Please try another.")

    tk.Button(root, text="Register", command=handle_signup).pack(pady=20)
    tk.Button(root, text="Back to Home", command=show_home_screen).pack(pady=10)

def show_home_screen():
    clear_screen()
    root.title("ChipIn App")
    tk.Label(root, text="Welcome to ChipIn", font=("Arial", 18)).pack(pady=20)
    tk.Button(root, text="User Login", command=lambda: login_screen("User Login Page")).pack(pady=10)
    tk.Button(root, text="Admin Login", command=lambda: login_screen("Admin Login Page", is_admin=True)).pack(pady=10)
    tk.Button(root, text="Sign Up", command=show_signup_screen).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

# Initialize Google Calendar API. new 4
authenticate_google_calendar()
# Main Window
root = tk.Tk()
root.geometry("900x600")  # Adjust window size
root.configure(bg="#f7f7f7")
show_home_screen()
root.mainloop()
