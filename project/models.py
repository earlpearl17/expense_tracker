from views import db

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, month, name, amount, user_id):
        self.month = month
        self.name = name
        self.amount = amount
        self.user_id = user_id

    def __repr__(self):
        return '<name {0}>'.format(self.name)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    expenses = db.relationship('Expense', backref='poster')
    role = db.Column(db.String, default='user')

    #def __init__(self, name=None, email=None, password=None):
    def __init__(self, name=None, email=None, password=None, role=None):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return '<User {0}>'.format(self.name)