# project/db_create.py
from views import db
from models import Expense#, User
from datetime import date

# create a new expenses table
db.create_all()

db.session.add(Expense("August", "Groceries", 300.00))
db.session.add(Expense("August", "Physio", 70.25))
#db.session.add(User("admin", "admin@gmail.com", "admin", "admin"))

# commit the changes
db.session.commit()

        