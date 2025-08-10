
import pandas as pd
import matplotlib.pyplot as plt
import stdiomask
from db.queries_sql import mycon, cursor,engine,engcon

from colorama import Fore, Style, init  # Style.BRIGHT (NORMAL OR ), Fore.GREEN, Fore.RED, Fore.YELLOW
init(autoreset=True)

def user_rejisteration():
    while True:
        name = input(f"{Style.BRIGHT}{Fore.YELLOW}ENTER YOUR NAME: ").strip()
        if name.replace(" ", "").isalpha():
            break
        print(f"{Style.BRIGHT}{Fore.RED}❌ INVALID NAME. Please enter a valid name (letters only).")

    while True:
        email = input(f"{Style.BRIGHT}{Fore.YELLOW}ENTER YOUR EMAIL: ").strip()
        # Simple email regex
        if '@' in email and '.' in email:
            break
        print(f"{Style.BRIGHT}{Fore.RED}❌ INVALID EMAIL. Please enter a valid email address.")

    while True:
        phone = input(f"{Style.BRIGHT}{Fore.YELLOW}ENTER YOUR PHONE NUMBER: ").strip()
        if phone.isdigit() and len(phone) in [10, 11, 12]:
            break
        print(f"{Style.BRIGHT}{Fore.RED}❌ INVALID PHONE NUMBER. Please enter a valid number (10-12 digits).")

    address = input(f"{Style.BRIGHT}{Fore.YELLOW}ENTER YOUR ADDRESS: ").strip()
    city = input(f"{Style.BRIGHT}{Fore.YELLOW}ENTER YOUR CITY: ").strip()
    state = input(f"{Style.BRIGHT}{Fore.YELLOW}ENTER YOUR STATE: ").strip()
    while True:
        username = input(f"{Style.BRIGHT}{Fore.YELLOW}CREATE YOUR NEW USERNAME: ").strip()
        if username:
            break
        print(f"{Style.BRIGHT}{Fore.RED}❌ USERNAME CANNOT BE EMPTY.")
    
    while True:
        password = stdiomask.getpass(prompt=f"{Style.BRIGHT}{Fore.YELLOW}ENTER NEW PASSWORD: ", mask='*')
        confirm_password = stdiomask.getpass(prompt=f"{Style.BRIGHT}{Fore.YELLOW}CONFIRM YOUR PASSWORD: ", mask='*')
        if len(password) < 6:
            print(f"{Style.BRIGHT}{Fore.RED}❌ PASSWORD TOO SHORT. Must be at least 6 characters.")
            continue
        if password != confirm_password:
            print(f"{Style.BRIGHT}{Fore.RED}❌ PASSWORDS DO NOT MATCH. Please try again.")
            continue
        break
    Entry_df = pd.DataFrame({  # I AM USING SCALAR VALUES HERE SO THEREFORE [ ] is mandatory
        'name': [name],
        'email': [email],
        'phone': [phone],
        'address': [address],
        'city': [city],
        'state': [state],
        'username': [username],
        'password': [password]
    })
    Entry_df.to_sql('users', con=engcon, if_exists='append', index=False)
    print(f"{Style.BRIGHT}{Fore.GREEN}✅ REGISTRATION SUCCESSFUL! You can now log in.")

def user_login():
    while True:
        username = input(f"{Style.BRIGHT}{Fore.YELLOW}ENTER YOUR USERNAME or Email: ").strip()
        password = stdiomask.getpass(prompt=f"{Style.BRIGHT}{Fore.YELLOW}ENTER YOUR PASSWORD: ", mask='*')
        
        if username and password:  # Placeholder for actual authentication logic
            query = """
                SELECT * FROM users 
                WHERE (username = %s OR email = %s) AND password = %s
            """
            logindf = pd.read_sql(query, con=engcon, params=(username, username, password))

            if not logindf.empty:
                print(f"\n{Style.BRIGHT}{Fore.GREEN}✅ LOGIN SUCCESSFUL!\n")
                print(logindf[['user_id', 'username', 'user_role']])  # Show some user info
                user_dashboard()  # Proceed to dashboard
                break
            else:
                print(f"\n{Style.BRIGHT}{Fore.RED}❌ INVALID CREDENTIALS. Please try again.\n")
                k = input(f"{Style.DIM}{Fore.YELLOW}Press Enter to try again or type 'exit' to quit: ")
                if k.lower() == 'exit':
                    print(f"{Style.BRIGHT}{Fore.RED}Exiting login.")
                    return
        else:
            print(f"\n{Style.BRIGHT}{Fore.RED}❌ Both fields are required.\n")

def user_dashboard():
    pass


    #SAVE USERNAME TO DATABASE


