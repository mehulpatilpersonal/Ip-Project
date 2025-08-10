
from db.queries_sql import sql_connect, mycon, cursor, engcon
import pandas as pd
import matplotlib.pyplot as plt
from colorama import Fore, Style, init  # Style.BRIGHT (NORMAL OR ), Fore.GREEN, Fore.RED, Fore.YELLOW
init(autoreset=True)

def admin_login():
    init(autoreset=True)
    while True:
        username = input(f"{Style.BRIGHT}{Fore.YELLOW}ENTER ADMIN USERNAME: ")
        password = input(f"{Style.BRIGHT}{Fore.YELLOW}ENTER ADMIN PASSWORD: ")
        if username and password:
            query = """select * from users where username=%s and password=%s and user_role='admin'"""
            df = pd.read_sql(query, con=engcon, params=(username, password))
            if not df.empty:
                print(f"\n{Style.BRIGHT}{Fore.GREEN}✅ ADMIN LOGIN SUCCESSFUL!\n")
                print(df[['user_id', 'username', 'user_role']])
                admin_dashboard()  # Call the admin dashboard function
                break
        else:
            print(f"{Style.BRIGHT}{Fore.RED}❌ Invalid credentials, please try again.")
            k = input(f"{Style.DIM}{Fore.YELLOW}Press Enter to continue... or 'exit' to quit: ")
            if k.lower() == 'exit':
                print(f"{Style.BRIGHT}{Fore.RED}Exiting login.")
                return

def admin_dashboard():
    pass
