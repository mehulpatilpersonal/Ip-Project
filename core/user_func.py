
import pandas as pd
import metaplotlib.pyplot as plt
import stdiomask

def user_rejisteration():
    name = input("ENTER YOUR NAME: ")
    if name.isalpha():
        email = input("ENTER YOUR EMAIL: ")
    if '@' in email and '.' in email:
        phone = int(input("ENTER YOUR PHONE NUMBER: "))
    if phone.isdigit():
        Address = input("ENTER YOUR ADDRESS: ")
    username = input("CREATE YOUR NEW USERNAME: ")
    #password = input("ENTER NEW PASSWORD: ")
    password = stdiomask.getpass(prompt="ENTER NEW PASSWORD: ", mask='*')

    #SAVE USERNAME TO DATABASE

def user_login():
    username = input("ENTER USERNAME: ")
    password = stdiomask.getpass(prompt="ENTER NEW PASSWORD: ", mask='*')
def user_dashboard():
    pass
