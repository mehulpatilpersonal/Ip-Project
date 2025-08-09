
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

def main_func():
    while True:
        print("\nWELCOME TO VEHICLE MANAGEMENT SYSTEM")
        print("PLEASE SELECT FROM THE GIVEN OPTION:")
        print(" 1. NEW USER")
        print(" 2. OLD USER")
        print(" 3. ADMIN")
        print(" 4. EXIT")
        try:
            choice = int(input("\nEnter your choice (1-4): "))
        except ValueError:
            print("\nINVALID INPUT. Please enter a number between 1 and 4.\n")
            input("Press Enter to continue...")
            continue

        if choice == 1:
            print("\nWELCOME NEW USER\n")
            user_rejisteration()
        elif choice == 2:
            print("\nWELCOME OLD USER\n")
            user_login()
        elif choice == 3:
            print("\nWELCOME ADMIN\n")
            admin_login()
        elif choice == 4:
            print("\nTHANK YOU FOR USING VEHICLE MANAGEMENT SYSTEM\n")
            break
        else:
            print("\nINVALID CHOICE, PLEASE TRY AGAIN\n")
            input("Press Enter to continue...")



if __name__ == '__main__':
    #run_output_in_new_terminal()
   sql_connect()  
   print("CONNECTING TO DATABASE....")
   time.sleep(2)  # Simulate a delay for connection
   create_database()
   create_tables()  # Create tables in the database
   main_func() #MAIN FUNCTION CALL KAR DIA


