from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User
import re

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])
    nickname = StringField("Nazwa użytkownika", validators=[
        DataRequired(),
        Length(min=3, max=64)
    ])
    password = PasswordField("Hasło", validators=[
        DataRequired(),
        Length(min=8, message="Hasło musi mieć minimum 8 znaków.")
    ])
    password2 = PasswordField("Powtórz hasło", validators=[
        DataRequired(),
        EqualTo("password", message="Hasła muszą być takie same.")
    ])
    submit = SubmitField("Utwórz konto")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Ten e-mail jest już zajęty.")

    def validate_nickname(self, nickname):
        if User.query.filter_by(nickname=nickname.data).first():
            raise ValidationError("Ta nazwa użytkownika jest zajęta.")

    def validate_password(self, password):
        """Enhanced password validation with security requirements"""
        if not password.data:
            return
        
        pwd = password.data
        
        # Check minimum length
        if len(pwd) < 8:
            raise ValidationError("Hasło musi mieć minimum 8 znaków.")
        
        # Check for uppercase letter
        if not re.search(r'[A-Z]', pwd):
            raise ValidationError("Hasło musi zawierać przynajmniej jedną wielką literę.")
        
        # Check for lowercase letter
        if not re.search(r'[a-z]', pwd):
            raise ValidationError("Hasło musi zawierać przynajmniej jedną małą literę.")
        
        # Check for digit
        if not re.search(r'[0-9]', pwd):
            raise ValidationError("Hasło musi zawierać przynajmniej jedną cyfrę.")
        
        # Check for special character
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', pwd):
            raise ValidationError("Hasło musi zawierać przynajmniej jeden znak specjalny (!@#$%^&*).")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Hasło", validators=[DataRequired()])
    submit = SubmitField("Zaloguj")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Obecne hasło", validators=[
        DataRequired(message="Musisz podać obecne hasło.")
    ])
    new_password = PasswordField("Nowe hasło", validators=[
        DataRequired(),
        Length(min=8, message="Hasło musi mieć minimum 8 znaków.")
    ])
    new_password2 = PasswordField("Powtórz nowe hasło", validators=[
        DataRequired(),
        EqualTo("new_password", message="Hasła muszą być takie same.")
    ])
    submit = SubmitField("Zmień hasło")

    def validate_new_password(self, new_password):
        """Enhanced password validation with security requirements"""
        if not new_password.data:
            return
        
        pwd = new_password.data
        
        # Check minimum length
        if len(pwd) < 8:
            raise ValidationError("Hasło musi mieć minimum 8 znaków.")
        
        # Check for uppercase letter
        if not re.search(r'[A-Z]', pwd):
            raise ValidationError("Hasło musi zawierać przynajmniej jedną wielką literę.")
        
        # Check for lowercase letter
        if not re.search(r'[a-z]', pwd):
            raise ValidationError("Hasło musi zawierać przynajmniej jedną małą literę.")
        
        # Check for digit
        if not re.search(r'[0-9]', pwd):
            raise ValidationError("Hasło musi zawierać przynajmniej jedną cyfrę.")
        
        # Check for special character
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', pwd):
            raise ValidationError("Hasło musi zawierać przynajmniej jeden znak specjalny (!@#$%^&*).")

