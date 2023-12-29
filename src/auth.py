from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message

from src.models import Organizer, User, db
from src.mail import send_email
from src.forms import ResetPasswordRequestForm, ResetPasswordForm
from src import app
from src.mail import mail
from src import logger


@app.route('/login')
def login():
    return render_template('auth/login.html')


@app.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(name=name, password=password).first()
    if not user:
        flash('Проверьте ваше имя и пароль.', 'info')
        return redirect(url_for('login'))
    login_user(user, remember=remember)
    logger.info(f'Вход "{name}"')
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        user = User.query.filter_by(name=name).first()
        if user:
            flash('Уже есть пользователь с таким же именем!', 'info')
            return render_template('auth/register.html')
        else:
            first_user = User.query.all()
            is_admin = False if first_user else True
            new_user = User(name=name, password=password, email=email, is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()
            logger.info(f'Добавлен пользователь "{name}"')
            flash('Аккаунт успешно создан', 'success')
            context = {'name': name, 'password': password}
            msg = Message('Уведомление о регистрации', [email])
            msg.html = render_template('mail/yvedoml.html', **context)
            print(msg.html)
            try:
                mail.send(msg)
            except Exception:
                logger.info(f'Ошибка при попытке отправки email на {email} для "{name}"')
            else:
                logger.info(f'На {email} послано "Уведомление о регистрации" для "{name}"')
            return redirect(url_for('login'))
    return render_template('auth/register.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', name=current_user.name)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    sender = app.config['ADMINS'][0]
    recipients = [user.email]
    text_body = render_template('auth/reset_password.txt', user=user, token=token)
    html_body = render_template('auth/reset_password.html', user=user, token=token)
    send_email('[Наш сайт] сброс пароля', sender=sender, recipients=recipients, text_body=text_body, html_body=html_body)
    logger.info(f'Послано письмо с токеном сброса пароля - {recipients}')


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Проверьте вашу почту с инструкцией для сброса пароля', 'info')
        return redirect(url_for('login'))
    return render_template('auth/reset_password_request.html', title='Сброс пароля', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ваш пароль изменен.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/reset_password_2.html', form=form)
