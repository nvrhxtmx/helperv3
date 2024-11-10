from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User
from .forms import EditUserForm
from .extensions import db
from werkzeug.security import check_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/updates')
def updates():
    return render_template('updates.html')

# Страница с подробным описанием обновлений
@main.route('/update_detail<number>')
def update_detail(number):
    try:
        # Проверяем, существует ли файл с нужным шаблоном
        return render_template(f'update_detail{number}.html')
    except:
        # Если файл не найден, выводим страницу с ошибкой
        return render_template('404.html'), 404

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditUserForm(obj=current_user)
    if form.validate_on_submit():
        # Проверка, существует ли уже аккаунт с таким же email
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user and existing_user.id != current_user.id:
            flash('Аккаунт с таким email уже существует', 'error')
        elif not check_password_hash(current_user.password, form.password.data):
            flash('Неверный пароль', 'error')
        else:
            # Обновляем данные пользователя
            current_user.email = form.email.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            db.session.commit()
            flash('Профиль успешно обновлен', 'success')
            return redirect(url_for('main.profile'))
    return render_template('edit_profile.html', form=form)

@main.route('/admin_users')
@login_required
def admin_users():
    if current_user.email != 'nvrhxtmx@gmail.com':
        return "Access Denied", 403
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@main.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.email != 'admin':
        return "Access Denied", 403
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for('main.admin_users'))
    return render_template('edit_user.html', form=form, user=user)