# project/db_migrate.py

# from views import db
# from _config import DATABASE_PATH
# import sqlite3

# #TO UPDATE expenses TABLE
# with sqlite3.connect(DATABASE_PATH) as connection:
#     # get a cursor object used to execute SQL commands
#     c = connection.cursor()
    
#     # temporarily change the name of expenses table
#     c.execute("""ALTER TABLE expenses RENAME TO old_expenses""")
    
#     # recreate a new expenses table with updated schema
#     db.create_all()
#     # c.execute("""CREATE TABLE expenses(
#     #     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     #     month TEXT NOT NULL,
#     #     name TEXT NOT NULL, 
#     #     amount FLOAT NOT NULL
#     #     )
#     # """)

#     # retrieve data from old_expenses table
#     c.execute("""SELECT month, name, amount FROM old_expenses ORDER BY id ASC""")
    
#     # save all rows as a list of tuples; set posted_date to now and user_id to 1
#     data = [(row[0], row[1], row[2], 1) for row in c.fetchall()]
    
#     # insert data to expenses table
#     c.executemany("""INSERT INTO expenses (month, name, amount, user_id) VALUES (?, ?, ?, ?)""", data)
    
#     # delete old_expenses table
#     c.execute("DROP TABLE old_expenses")
from _config import DATABASE_PATH
from views import db
#from models import User
import sqlite3


# TO UPDATE USERS TABLE
with sqlite3.connect(DATABASE_PATH) as connection:
    # get a cursor object used to execute SQL commands
    c = connection.cursor()
    # temporarily change the name of users table
    c.execute("""ALTER TABLE users RENAME TO old_users""")
    # recreate a new users table with updated schema
    db.create_all()
    # retrieve data from old_users table
    c.execute("""SELECT name, email, password
                FROM old_users
                ORDER BY id ASC""")
    # save all rows as a list of tuples; set role to 'user'
    data = [(row[0], row[1], row[2],
            'user') for row in c.fetchall()]
    # insert data to users table
    c.executemany("""INSERT INTO users (name, email, password,
                    role) VALUES (?, ?, ?, ?)""", data)
    # delete old_users table
    c.execute("DROP TABLE old_users")


