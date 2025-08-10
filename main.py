
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
from db.tables_create import create_tables,create_database
from db.queries_sql import sql_connect
from colorama import Fore, Style, init  # Style.BRIGHT (NORMAL OR ), Fore.GREEN, Fore.RED, Fore.YELLOW
init(autoreset=True)

def main_func():
    while True:
        print(f"\n{Style.BRIGHT}{Fore.CYAN}WELCOME TO VEHICLE MANAGEMENT SYSTEM")
        print(f"{Style.BRIGHT}{Fore.YELLOW}PLEASE SELECT FROM THE GIVEN OPTION:")
        print(f"{Style.BRIGHT}{Fore.GREEN} 1. NEW USER")
        print(f"{Style.BRIGHT}{Fore.GREEN} 2. OLD USER")
        print(f"{Style.BRIGHT}{Fore.GREEN} 3. ADMIN")
        print(f"{Style.BRIGHT}{Fore.RED} 4. EXIT")
        try:
            choice = int(input(f"\n{Style.BRIGHT}{Fore.YELLOW}Enter your choice (1-4): "))
        except ValueError:
            print(f"\n{Style.BRIGHT}{Fore.RED}❌ INVALID INPUT. Please enter a number between 1 and 4.\n")
            input(f"{Style.DIM}{Fore.YELLOW}Press Enter to continue...")
            continue

        if choice == 1:
            print(f"\n{Style.BRIGHT}{Fore.GREEN}WELCOME NEW USER\n")
            user_rejisteration()
        elif choice == 2:
            print(f"\n{Style.BRIGHT}{Fore.GREEN}WELCOME OLD USER\n")
            user_login()
        elif choice == 3:
            print(f"\n{Style.BRIGHT}{Fore.GREEN}WELCOME ADMIN\n")
            admin_login()
        elif choice == 4:
            print(f"\n{Style.BRIGHT}{Fore.CYAN}THANK YOU FOR USING VEHICLE MANAGEMENT SYSTEM\n")
            break
        else:
            print(f"\n{Style.BRIGHT}{Fore.RED}❌ INVALID CHOICE, PLEASE TRY AGAIN\n")
            input(f"{Style.DIM}{Fore.YELLOW}Press Enter to continue...")

if __name__ == '__main__':
    #run_output_in_new_terminal()
   sql_connect()  
   print("CONNECTING TO DATABASE....")
   time.sleep(2)  # Simulate a delay for connection
   create_database()
   create_tables()  # Create tables in the database
   main_func() #MAIN FUNCTION CALL KAR DIA


