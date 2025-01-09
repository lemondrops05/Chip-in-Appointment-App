import tkinter as tk
from tkinter import messagebox
import sqlite3
import time
from chipin_data import add_user

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

# Main Window
root = tk.Tk()
root.geometry("900x600")  # Adjust window size
root.configure(bg="#f7f7f7")
show_home_screen()
root.mainloop()
