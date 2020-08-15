# project/views.py

from forms import AddExpenseForm
from functools import wraps
from flask import Flask, flash, redirect, render_template, \
        request, session, url_for
from flask_sqlalchemy import SQLAlchemy

# config
app = Flask(__name__)
#app.config.from_object('_config')
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)
from models import Expense#, User

# helper functions
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# route handlers
@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('Goodbye!')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] \
                or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            flash('Welcome!')
            return redirect(url_for('expenses'))
    return render_template('login.html')

@app.route('/expenses/')
@login_required
def expenses():
    open_expenses = db.session.query(Expense)\
        .order_by(Expense.id.asc())
    return render_template(
        'expenses.html',
        form=AddExpenseForm(request.form),
        open_expenses=open_expenses
    )    

# Add new expenses
@app.route('/add/', methods=['GET','POST'])
@login_required
def new_expense():
    form = AddExpenseForm(request.form)
    flash("Month: " + form.month.data)
    #if request.method == 'POST' and form.validate():
    # if not form.validate_on_submit():
    #     return render_template('expenses.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_expense = Expense(
                form.month.data,
                form.name.data,
                form.amount.data,
            )
            db.session.add(new_expense)
            db.session.commit()
            flash('New expense was successfully added.')
        else:
            #flash('ERROR')
            flash("Form Errors: " + str(form.errors))
    return redirect(url_for('expenses'))

# #Update Expense Amounts REVISIT
# @app.route('/update/<int:expense_id>/', methods=['GET', 'POST'])
# @login_required
# def update(expense_id):
#     #new_id = expense_id
#     expense = Expense.query.get(expense_id)
#     if request.method == 'GET':
#         return render_template(
#             'update.html',
#             form = AddExpenseForm(obj=expense)
#         )   
    # else:
    #     db.session.merge(expense)    
    #     flash("Expense has been updated.")
    #     redirect(url_for('expenses'))
         
    
    #db.session.query(Expense).filter_by(id=new_id).update({"amount": "100"})
    #db.session.commit()
    #flash('The expense was updated.')
    #return redirect(url_for('expenses'))
        

# Delete Expenses
@app.route('/delete/<int:expense_id>/')
@login_required
def delete(expense_id):
    new_id = expense_id
    db.session.query(Expense).filter_by(id=new_id).delete()
    db.session.commit()
    flash('The expense was successfully deleted.')
    return redirect(url_for('expenses'))

# #Update Expense Amounts REVISIT
# @app.route('/update/<int:expense_id>/', methods=['GET', 'POST'])
# @login_required
# def update(expense_id):
#     g.db = connect_db()
#     cursor = g.db.execute(
#         'select id, month, name, amount from expenses where id='+str(expense_id)
#     )
#     open_expense = [
#         dict(id=row[0], month=row[1], name=row[2], amount=row[3]) for row in cursor.fetchall()
#     ]
#     #open_expense = cursor.fetchone()

#     g.db.close()
    
#     return render_template(
#         'update.html',
#         #expense_id=expense_id,
#         #expense_id=open_expense[0],
#         #form=AddExpenseForm()
#         open_expense=open_expense,
#         form=AddExpenseForm(request.form)
#         #form = AddExpenseForm(data=open_expense[0])
#         #form = AddExpenseForm(obj=open_expense)
#     )    

# #Update Expense Amounts REVISIT
# @app.route('/update/<int:expense_id>/')
# @login_required
# def update(expense_id):
#     g.db = connect_db()
#     #stmt = update expenses set amount = ' + str(request.form['amount']) + ' where id='+str(expense_id) 
#     stmt = 'update expenses set amount = 200 where id='+str(expense_id) 
#     g.db.execute(stmt)
#     # g.db.execute(
#     #     'update expenses set amount = ' + str(request.form['amount']) + ' where id='+str(expense_id)
#     # )
#     g.db.commit()
#     g.db.close()
#     flash('The expense amount was updated.')
#     return redirect(url_for('expenses'))    

# # Delete Expenses
# @app.route('/delete/<int:expense_id>/')
# @login_required
# def delete(expense_id):
#     g.db = connect_db()
#     g.db.execute('delete from expenses where id='+str(expense_id))
#     g.db.commit()
#     g.db.close()
#     flash('The expense was deleted.')
#     return redirect(url_for('expenses'))    

