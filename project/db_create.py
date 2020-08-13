# project/db_create.py
import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    # get a cursor object used to execute SQL commands
    c = connection.cursor()
    # create the table
    c.execute("""CREATE TABLE expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT NOT NULL,
        name TEXT NOT NULL, 
        amount FLOAT NOT NULL)
    """)
    
    # insert dummy data into the table
    c.execute(
        'INSERT INTO expenses (month, name, amount)'
        'VALUES("August", "Groceries", 300.00)'
    )
    c.execute(
        'INSERT INTO expenses (month, name, amount)'
        'VALUES("August", "Internet", 34.95)'
    )
    