# project/forms.py
from flask_wtf import Form
#from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, \
        SelectField, FloatField
from wtforms.validators import DataRequired

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
    name = StringField('Expense', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()]) 
    user_id = IntegerField()
    # def validate_amount(form, field):
    #     if not re.match(check, field.data):
    #         raise ValidationError("Please supply a valid expense amount.")
    