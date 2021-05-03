#Imports
import sqlite3
import time
# Connect to SQLite3 Database
conn = sqlite3.connect('Employee_data.db')

# Create a cursor
c = conn.cursor()

# create a user_data table 
c.execute("CREATE TABLE IF NOT EXISTS User_data (Idno text PRIMARY KEY,first_name text ,user_name text ,email_id text ,department text )")
conn.commit()
#Display
c.execute("SELECT rowid, * FROM User_data")

#create a present table 
c.execute("CREATE TABLE IF NOT EXISTS Present_table (Idno text PRIMARY KEY,first_name text ,user_name text ,email_id text ,department text )")
c.execute("SELECT rowid, * FROM User_data")	
#commit our command 
conn.commit()

#close connection
conn.close()