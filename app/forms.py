from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

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


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Hasło", validators=[DataRequired()])
    submit = SubmitField("Zaloguj")

