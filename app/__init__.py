# __init__.py
import os
from flask import Flask, render_template, session
from .extensions import db, login_manager, migrate
from werkzeug.security import generate_password_hash
from .models import User
import logging
from flask_wtf.csrf import CSRFProtect

logging.basicConfig(level=logging.DEBUG)

def create_app():
    app = Flask(__name__)
    
    # Генерация SECRET_KEY, если он не установлен
    if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = os.urandom(24)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение предупреждений от SQLAlchemy
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf = CSRFProtect(app)  # Включение CSRF-защиты

    @app.before_request
    def make_session_permanent():
        session.permanent = True  # Установите сессии постоянными

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Создание таблиц и административного пользователя
    with app.app_context():
        db.create_all()  # Создание всех таблиц
        admin_user = User.query.filter_by(email='nvrhxtmx@gmail.com').first()
        if not admin_user:
            hashed_password = generate_password_hash('lchxncx68', method='pbkdf2:sha256:600000')
            logging.debug(f"Hashed password for admin: {hashed_password}")
            admin_user = User(email='nvrhxtmx@gmail.com', first_name='Admin', last_name='Admin', password=hashed_password)
            db.session.add(admin_user)
            db.session.commit()

    # Регистрация блюпринтов
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Обработка ошибок
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app