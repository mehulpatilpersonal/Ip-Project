from core.admins import admin_login
from core.user_func import user_rejisteration, user_login   
# import subprocess
# import platform
# import time

# def run_output_in_new_terminal():
#     script = 'output.py'
#     system = platform.system()

#     if system == 'Windows':
#         # Open new Command Prompt window and run output.py
#         subprocess.Popen(['start', 'cmd', '/k', f'python {script}'], shell=True)

def main_func():
   while True:
      print("WELCOME TO VEHICLE MANAGEMENT SYSTEM")
      choice=int(input("PLEASE SELECT FROM THE GIVEN OPTION \n\n 1. NEW USER \n\n 2.OLD USER \n\n 3. ADMIN \n\n 4. EXIT  \n\n"))
      if choice ==1:
         print("\n\n WELCOME NEW USER \n\n")
         user_rejisteration() # handle new user registration
         pass
         
      if choice == 2:
         print("\n\n WELCOME OLD USER \n\n")
         user_login()#call the function to handle old user login
         pass
         
      if choice == 3:
         print("\n\n WELCOME ADMIN \n\n")
         admin_login() #call the function to handle admin login
         pass
         
      if choice ==4:
         print("\n\n THANK YOU FOR USING VEHICLE MANAGEMENT SYSTEM \n\n")
         exit()
      else:
         print("\n\n INVALID CHOICE, PLEASE TRY AGAIN \n\n")
      
      


if __name__ == '__main__':
    #run_output_in_new_terminal()
    main_func() #MAIN FUNCTION CALL KAR DIA

    #time.sleep(500)  # Optional: wait a bit before running the script
