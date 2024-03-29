from flask_wtf import FlaskForm
## from flask_wtf.file import FileField, FileAllowed 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
## from flask_login import current_user
from marketplace.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username is taken, Please choose a different one')

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('Email is taken, Please make use of a different one')


class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

"""class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken, Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken, Please make use of a different one')

# Request and Reset password forms
class RequestResetForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
"""

class PurchaseItemForm(FlaskForm):
    submit = SubmitField('Purchase')
    

class SellItemForm(FlaskForm):
    submit = SubmitField('Sell')
    
class DeleteItemForm(FlaskForm):
    submit = SubmitField('YES')


class ItemForm(FlaskForm):
    name = StringField('Product Name', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    description = TextAreaField('Product Description', 
                           validators=[DataRequired(), Length(min=4, max=1024)])
    """barcode = StringField('Barcode', 
                           validators=[DataRequired(), Length(min=8, max=12)])"""
    price = IntegerField('Cost of Product')
    submit = SubmitField('Post Item')
    
class UpdateItemForm(FlaskForm):
    name = StringField('Product Name', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    description = TextAreaField('Product Description', 
                           validators=[DataRequired(), Length(min=4, max=1024)])
    price = IntegerField('Cost of Product')
    submit = SubmitField('Update Product')
