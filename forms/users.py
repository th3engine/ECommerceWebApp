from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField, SubmitField, PasswordField, EmailField, RadioField
from wtforms.validators import DataRequired, URL, Email, EqualTo, Length, InputRequired


class UserLogin(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(),Email()],render_kw={"placeholder":"name@example.com"})
    password = PasswordField("Password ",validators=[DataRequired()],render_kw={"placeholder":"password"})
    submit = SubmitField("Sign In")


class RegisterUser(FlaskForm):
    first_name = StringField("First Name:",validators=[DataRequired()])
    email = EmailField("Email: ",validators=[DataRequired(),Email()])
    password = PasswordField("Password:", validators=[DataRequired(),EqualTo('confirm',"Passwords must match")])
    confirm = PasswordField("Confirm Password:", validators=[DataRequired(),EqualTo('password',"Passwords must match")])
    submit = SubmitField("Register")