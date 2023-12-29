import os
from flask_mail import Message
from threading import Thread
from flask import flash, render_template
from src.models import User, Event

from src import app
from src import mail
from src import logger


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    print(msg.html)
    try:
        mail.send(msg)
    except:
        logger.info(f'Ошибка при отправке email')


def async_email(app1, msg):
    with app1.app_context():
        print(msg.html)
        try:
            mail.send(msg)
        except:
            logger.info(f'Ошибка при отправке email')


@app.route("/send_mail_async")
def send_mail_async():
    msg = Message('Тест асинхронной посылки письма', ['vyatdima@yandex.ru'])
    msg.html = '<h1>Асинхронная посылка</h1>'
    thr = Thread(target=async_email, args=(app, msg))
    thr.start()
    return render_template('index.html', list_events=Event.query.all())


@app.route("/send_mail_test")
def send_mail_test():
    msg = Message('', ['vyatdima@yandex.ru'])
    msg.html = 'privet'
    print(msg.html)
    try:
        mail.send(msg)
    except:
        logger.info(f'Ошибка при отправке email')
        flash('Ошибка при отправке email', 'danger')
    else:
        flash('Письмо отправлено', 'success')
    return render_template('index.html', list_events=Event.query.all())


@app.route("/send_mail_for_all_users")
def send_mail_for_all_users():
    list_users = User.query.all()
    flag = False
    for user in list_users:
        context = {'name': user.name, 'password': user.password}
        msg = Message('Массовая рассылка', [user.email])
        msg.html = render_template('mail/yvedoml.html', **context)
        print(msg.html)
        try:
            mail.send(msg)
            flag = True
        except:
            pass
    if flag:
        logger.info(f'Ошибка при отправке email')
        flash('Ошибка при отправке email', 'danger')
    else:
        flash('Письма отправлены', 'success')
    return render_template('index.html', list_events=Event.query.all())


@app.route("/send_mail_with_attach")
def send_mail_with_attach():
    context = {'name': 'Дмитрий', }
    msg = Message('Тест посылки асинхронного письма', ['vyatdima@yandex.ru'])
    msg.html = render_template('mail/test.html', **context)
    attach_file = 'default.jpg'
    attach_path = '\\static\\images\\'
    basedir = os.path.abspath(os.path.dirname(__file__))
    attach_full_path = f"{basedir}{attach_path}{attach_file}"
    if attach_full_path:
        with app.open_resource(attach_full_path) as fp:
            msg.attach(attach_full_path, "image/png", fp.read())
    print(msg.html)
    try:
        mail.send(msg)
    except:
        logger.info(f'Ошибка при отправке email')
        flash('Ошибка при отправке email', 'danger')
    else:
        flash('Письмо отправлено', 'success')
    return render_template('index.html', list_events=Event.query.all())
