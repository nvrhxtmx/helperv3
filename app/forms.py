# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from email_validator import validate_email, EmailNotValidError

class LoginForm(FlaskForm):
    email = StringField('', validators=[DataRequired(), Email()])
    password = PasswordField('', validators=[DataRequired()])
    submit = SubmitField('Войти', render_kw= {'class': 'btn'})

class RegisterForm(FlaskForm):
    email = StringField('', validators=[DataRequired()])
    first_name = StringField('', validators=[DataRequired()])
    last_name = StringField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    confirm_password = PasswordField('', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться', render_kw= {'class': 'btn'})

    def validate_email(self, field):
        if field.data != 'nvrhxtmx@gmail.com':
            try:
                validate_email(field.data)
            except EmailNotValidError as e:
                raise ValueError('Invalid email address')

class EditUserForm(FlaskForm):
    email = StringField('', validators=[DataRequired(), Email()])
    first_name = StringField('', validators=[DataRequired()])
    last_name = StringField('', validators=[DataRequired()])
    password = PasswordField('')
    submit = SubmitField('Сохранить изменения', render_kw= {'class': 'btn'})