
import mysql.connector as sql
from sqlalchemy import create_engine
import pymysql

def sql_connect():
    # mycon = sql.connect(host="ipaddress", user="garage",password="StrongPass123!",database="vehiclemanagement")
    mycon = sql.connect(host="localhost", user="root", password="123456", database="vehiclemanagement")

    cursor = mycon.cursor() 
    mycon.autocommit = False # Ensures queries are not committed automaticallu. You’ll need to call mycon.commit() or mycon.rollback().
    mycon.start_transaction(isolation_level='READ COMMITTED')# Sets the isolation level for the transaction.# Prevents dirty reads.
        
    engine = create_engine("mysql+pymysql://root:123456@localhost/vehiclemanagement",isolation_level="AUTOCOMMIT",#echo=True ONLY FOR DEBUGGING
    ) #READ COMMITED WAS NOT WORKING FOR TO_SQL , ONLY WORKING FOR READ SQL QUERY, NOW AUTOCOMMIT IS WORKING FINE FOR TO_SQL AND READ SQL BOTH 
     # I TRIED without AUTOCOMMIT THE CONNECTION WAS NOT COMMITING THE DATA TO TABLES AUTOMATICALLY EITHER USING engine.begin() was the option with every query
     #OR I CAN USE AUTOCOMMIT IN ENGINE ITSELF, SO I CHOSE AUTOCOMMIT IN ENGINE ITSELF
    engcon=engine.connect()
    return mycon,cursor,engine,engcon

mycon,cursor,engine,engcon=sql_connect()





#       DOCS FOR isloation level ? Why i used Isolation level = "READ COMMITTED"
# https://docs.sqlalchemy.org/en/20/dialects/mysql.html#mysql-isolation-level

# Permitted values are 'READ UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ','AUTO COMMITED' and 'SERIALIZABLE'. Means Isloation Level can be any of these or more are available.
"""✅ Use AUTO_COMMIT for:

   --->Read-only queries (searching services, viewing vehicles, checking invoices).

   --->Quick operations that don’t need rollback.

✅ Use READ_COMMITTED for:

  ---->Critical multi-step operations (service booking, payment, assigning mechanics).

  ---->When you want rollback on failure.

  ---->To avoid dirty reads when multiple users interact at once.

AUTO_COMMIT = safe & fast for simple reads.

READ_COMMITTED = better for transactions where consistency matters (bookings, payments)."""
