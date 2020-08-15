# project/forms.py
from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, \
SelectField, PasswordField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo, Email

# import re
# check = "^\d+(\.\d{0,2})?$"

class AddExpenseForm(Form):
#class AddExpenseForm(FlaskForm):
    id = IntegerField()
    month = SelectField(
        'Month',
        validators=[DataRequired()],
        choices=[
        ('January', 'January'), ('February', 'February'), ('March', 'March'), 
        ('April', 'April'), ('May', 'May'), ('June', 'June'), 
        ('July', 'July'), ('August', 'August'), ('September', 'September'), 
        ('October', 'October'), ('November', 'November'), ('December', 'December')
        ]
    )
    name = StringField(
        'Expense', validators=[DataRequired()])
    #amount = FloatField('Amount', validators=[DataRequired()]) 
    amount = DecimalField('Amount', validators=[DataRequired()]) 
    #user_id = IntegerField()
    # def validate_amount(form, field):
    #     if not re.match(check, field.data):
    #         raise ValidationError("Please supply a valid expense amount.")

class RegisterForm(Form):
    name = StringField(
        'Username',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )

class LoginForm(Form):
    name = StringField(
        'Username',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )