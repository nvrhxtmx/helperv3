# auth.py
import logging
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from .forms import LoginForm, RegisterForm
from .extensions import db

auth = Blueprint('auth', __name__)
logging.basicConfig(level=logging.DEBUG)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        logging.debug("Form submitted successfully.")
        email = form.email.data
        password = form.password.data
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            logging.debug(f"User logged in: {email}")
            login_user(user, remember=remember)
            return redirect(url_for('main.profile'))
        else:
            logging.debug(f"Invalid login attempt for user: {email}")
            flash('Пожалуйста, проверьте свои данные для входа и попробуйте снова.')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256:600000')
        new_user = User(email=email, first_name=first_name, last_name=last_name, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred while registering. Please try again.')
            return redirect(url_for('auth.register'))
        
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth.route('/terms')
def terms():
    return render_template('terms.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/test', methods=['GET', 'POST'])
def test():
    form = LoginForm()
    if form.validate_on_submit():
        logging.debug("Form is valid")
        return "Success!"
    else:
        logging.debug("Form errors: %s", form.errors)  # Логирование ошибок формы
    return render_template('test.html', form=form)