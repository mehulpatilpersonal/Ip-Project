import mysql.connector as sql

mycon = sql.connect(host="localhost", user="root", password="123456", database="vehiclemanagement")

cursor = mycon.cursor()

