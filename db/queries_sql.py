
import mysql.connector as sql
from sqlalchemy import create_engine
import pymysql

def sql_connect():
    mycon = sql.connect(host="localhost", user="root", password="123456", database="vehiclemanagement")

    cursor = mycon.cursor()

    engine = create_engine("mysql+pymysql://root:123456@localhost/vehiclemanagement",#echo=True ONLY FOR DEBUGGING
    )
    engcon=engine.connect()
    return mycon,cursor,engine,engcon

mycon,cursor,engine,engcon=sql_connect()