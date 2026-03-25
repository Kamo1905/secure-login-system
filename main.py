import tkinter as tk 
from tkinter import messagebox
import hashlib
import database
import re 

database.connect()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    username = username_entry.get()
    password = password_entry.get()
    strength = check_strength(password)

    if username == "" or password == "":
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    hashed = hash_password(password)

    if database.register_user(username, hashed):
        messagebox.showinfo("Success", "User Registered!")
    else:
        messagebox.showerror("Error", "Username already exists.")

    if strength < 2:
        messagebox.showerror("Weak Password", "Please use a stronger password")
        return

def login():
    username = username_entry.get()
    password = password_entry.get()

    hased = hash_password(password)

    if database.login_user(username, hased):
        open_dashboard(username)
    else:
        messagebox.showerror("Error", "Invalid username or password.")


def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
    else:
        password_entry.config(show='*')

def check_strength(password):
    strength = 0

    if len(password) >= 8:
        strength += 1
    if re.search("[A-Z]", password) and re.search("[a-z]", password):
        strength += 1
    if re.search("[0-9]", password):   
        strength += 1
    if re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        strength += 1

def clear_fields():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    clear_fields()

def open_dashboard(username):
    dash = tk.Toplevel(root)
    dash.title("Dashboard")

    tk.Label(dash, text=f"Welcome {username}!").pack()

# GUI 
root = tk.Tk()
root.title("Kamo's Secure Login System")

tk.Label(root, text="Username").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Register", command=register).pack()
tk.Button(root, text="Login", command=login).pack()
tk.Button(root, text="Show/Hide Password", command=toggle_password).pack()

root.mainloop()