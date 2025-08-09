

import pandas as pd
import matplotlib.pyplot as plt

def admin_login():
    username = input("ENTER ADMIN USERNAME: ")
    password = input("ENTER ADMIN PASSWORD: ")
    if username == "admin" and password == "admin123":
        print("Login successful!")
        admin_dashboard()  # Call the admin dashboard function
    else:
        print("Invalid credentials, please try again.")
        
def admin_dashboard():
    pass