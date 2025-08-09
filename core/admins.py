
from db.queries_sql import sql_connect, mycon, cursor, engcon
import pandas as pd
import matplotlib.pyplot as plt

def admin_login():
    while True:
        username = input("ENTER ADMIN USERNAME: ")
        password = input("ENTER ADMIN PASSWORD: ")
        if username and password:
            query= """select * from users where username=%s and password=%s and user_role='admin'"""
            df = pd.read_sql(query, con=engcon, params=(username, password))
            if not df.empty:
                print("\nADMIN LOGIN SUCCESSFUL!\n")
                print(df[['user_id', 'username', 'user_role']])
                admin_dashboard()  # Call the admin dashboard function
                break
        else:
            print("Invalid credentials, please try again.")
            k=input("Press Enter to continue... or 'exit' to quit: ")
            if k.lower() == 'exit':
                print("Exiting login.")
                return
        
def admin_dashboard():
    pass