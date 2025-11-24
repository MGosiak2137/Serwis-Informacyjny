from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    nickname = StringField("Nick", validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField("Hasło", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField("Powtórz hasło", validators=[
        DataRequired(),
        EqualTo("password", message="Hasła muszą być takie same")
    ])
    submit = SubmitField("Zarejestruj")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Hasło", validators=[DataRequired()])
    submit = SubmitField("Zaloguj")
