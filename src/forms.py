from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, EmailField, SubmitField, PasswordField, validators
from wtforms.validators import DataRequired, Email, EqualTo


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Адрес электронной почты:', validators=[DataRequired(), Email()])
    submit = SubmitField('Выслать письмо')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите новый пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Подтвердить смену пароля')


class UserEditForm(Form):
    is_admin = BooleanField('Администратор')
    name = StringField('Логин', validators=[validators.DataRequired()])
    email = EmailField('Email', validators=[validators.DataRequired()])
    password = StringField('Пароль')
    submit = SubmitField('Сохранить')
