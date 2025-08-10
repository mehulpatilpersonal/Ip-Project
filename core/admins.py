from db.queries_sql import sql_connect, mycon, cursor, engcon
import pandas as pd
import matplotlib.pyplot as plt
import stdiomask
from styles import *  # Import style constants


def admin_login():
    while True:
        username = input(f"{BRIGHT_YELLOW}ENTER ADMIN USERNAME: ")
        password = input(f"{BRIGHT_YELLOW}ENTER ADMIN PASSWORD: ")
        if username and password:
            query = """select * from users where username=%s and password=%s and user_role='admin'"""
            df = pd.read_sql(query, con=engcon, params=(username, password))
            if not df.empty:
                print(f"\n{BRIGHT_GREEN}✅ ADMIN LOGIN SUCCESSFUL!\n")
                print(df[['user_id', 'username', 'user_role']])
                admin_dashboard()  # Call the admin dashboard function
                break
        else:
            print(f"{BRIGHT_RED}❌ Invalid credentials, please try again.")
            k = input(f"{DIM_YELLOW}Press Enter to continue... or 'exit' to quit: ")
            if k.lower() == 'exit':
                print(f"{BRIGHT_RED}Exiting login.")
                return

def admin_dashboard():
    pass
