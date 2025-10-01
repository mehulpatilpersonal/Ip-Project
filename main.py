
# import subprocess
# import platform
# import time

# def run_output_in_new_terminal():
#     script = 'output.py'
#     system = platform.system()

#     if system == 'Windows':
#         # Open new Command Prompt window and run output.py
#         subprocess.Popen(['start', 'cmd', '/k', f'python {script}'], shell=True)
import time

from core.admins import admin_login
from core.user_func import user_rejisteration, user_login
from core.mechanic_func import mechanic_login
from db.tables_create import create_tables,create_database
from db.queries_sql import sql_connect

from styles import *  # Import all predefined styles (BRIGHT_GREEN, DIM_YELLOW, etc.)

def main_func():
    while True:
        # Main menu display
        print(f"\n{BRIGHT_CYAN}WELCOME TO VEHICLE MANAGEMENT SYSTEM 🔥🔥")
        print(f"{BRIGHT_YELLOW}PLEASE SELECT FROM THE GIVEN OPTION:")
        print(f"{BRIGHT_GREEN} 1. NEW USER")
        print(f"{BRIGHT_GREEN} 2. OLD USER")
        print(f"{BRIGHT_GREEN} 3. ADMIN")
        print(f"{BRIGHT_GREEN} 4. MECHANIC")
        print(f"{BRIGHT_RED} 5. EXIT")
        
        try:
            choice = int(input(f"\n{BRIGHT_YELLOW}Enter your choice (1-4): "))
        except ValueError:
            print(f"\n{BRIGHT_RED}❌ INVALID INPUT. Please enter a number between 1 and 4.\n")
            input(f"{DIM_YELLOW}Press Enter to continue...")
            continue

        if choice == 1:
            print(f"\n{BRIGHT_GREEN}WELCOME NEW USER\n")
            user_rejisteration()
        elif choice == 2:
            print(f"\n{BRIGHT_GREEN}WELCOME OLD USER\n")
            user_login()
        elif choice == 3:
            print(f"\n{BRIGHT_GREEN}WELCOME ADMIN\n")
            admin_login()
        elif choice ==4:
            print(f"\n{BRIGHT_GREEN}WELCOME MECHANIC\n")
            mechanic_login()
        elif choice == 5:
            print(f"\n{BRIGHT_CYAN}THANK YOU FOR USING VEHICLE MANAGEMENT SYSTEM\n")
            break
        else:
            print(f"\n{BRIGHT_RED}❌ INVALID CHOICE, PLEASE TRY AGAIN\n")
            input(f"{DIM_YELLOW}Press Enter to continue...")

if __name__ == '__main__':
    print(f"{BRIGHT_CYAN}INITIALIZING VEHICLE MANAGEMENT SYSTEM...")
    time.sleep(2)  # Simulate a delay for initialization
    sql_connect()  
    print(f"{BRIGHT_CYAN}CONNECTING TO DATABASE....")
    time.sleep(2)  # Simulate a delay for connection
    create_database()
    create_tables()  # Create tables in the database
    main_func()  # MAIN FUNCTION CALL KAR DIA


