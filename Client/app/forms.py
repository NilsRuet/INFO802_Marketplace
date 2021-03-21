from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, FloatField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    fn = StringField('First name',[DataRequired()])
    ln = StringField('Last name', [DataRequired()])
    submit = SubmitField("Log in")

class SignUpForm(FlaskForm):
    fn = StringField('First name',[DataRequired()])
    ln = StringField('Last name', [DataRequired()])
    submit = SubmitField("Sign Up")

class CreditCardForm(FlaskForm):
    cardNumber = StringField('Card number',[DataRequired()])
    cvx = StringField('CVX', [DataRequired()])
    expiration = StringField('Expiration date (MMAA)',[DataRequired()])
    submit = SubmitField("Save card")

class PayInForm(FlaskForm):
    amount = FloatField('Amount (€)', [DataRequired()])
    submit = SubmitField("Pay in")

class SellProductForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    description = StringField('Description (optional)')
    weight = FloatField('Weight (kg)', [DataRequired()])
    price = FloatField('Price (€)', [DataRequired()])
    submit = SubmitField("Confirm")

class BuyProductForm(FlaskForm):
    shippingDistance = FloatField('Shipping distance (km)')
    submit = SubmitField("Buy")

class ConfirmBuyProductForm(FlaskForm):
    submit = SubmitField("Confirm")