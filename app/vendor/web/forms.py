from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateField
from app.vendor.dao.user import UserDao


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = UserDao.get_by_email(email.data)
        if user is not None:
            raise ValidationError('Please use a different email address.')


class SoftwareForm(FlaskForm):
    software_name = StringField("Name", validators=[DataRequired()])
    provider = StringField("Vendor Name", validators=[DataRequired()])
    department = SelectField(
        'Department', [DataRequired()],
        choices=[('CorpIT', 'Corp IT'),
                 ('Sales', 'Sales'),
                 ('People', 'People'),
                 ('Finance', 'Finance'),
                 ('Marketing', 'Marketing'),
                 ('SRE', 'SRE'),
                 ('Product Management', 'Product Management')])

    budget_owner = SelectField(
        'Budget Owner', [DataRequired()],
        choices=[('CorpIT', 'Corp IT'),
                 ('Sales', 'Sales'),
                 ('People', 'People'),
                 ('Finance', 'Finance'),
                 ('Marketing', 'Marketing'),
                 ('SRE', 'SRE'),
                 ('Product Management', 'Product Management')])

    software_owner = StringField("Owner", validators=[DataRequired()])

    expiration_date = DateField("Expiration Date")

    payment_method = SelectField(
        'Payment Method', [DataRequired()],
        choices=[('Credit Card', 'Credit Card'),
                 ('Invoice', 'Invoice')])

    submit = SubmitField('Save')
