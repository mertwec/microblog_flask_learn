from datetime import datetime

from flask import render_template, redirect, \
    flash, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from guess_language import guess_language
from werkzeug.urls import url_parse

from app import db, current_app
from app.auth import bp
from app.auth.email import send_password_reset_email
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordForm
from app.auth.forms import ResetPasswordRequestForm
from app.models import User
from app.auth.email import send_password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        '''
        Kогда пользователь, не входящий в систему, обращается
        к функции просмотра, защищенной декодером @login_required,
        декоратор собирается перенаправить на страницу входа в систему, 
        но в это перенаправление будет включена дополнительная информация,
        чтобы приложение затем могло вернуться к первой странице. Если 
        пользователь переходит, например на /index, обработчик @login_required 
        перехватит запрос и ответит перенаправлением на /login, но он добавит 
        аргумент строки запроса к этому URL-адресу, сделав полный 
        URL /login?Next = /index. next аргумент строки запроса установлен на
        исходный URL-адрес, поэтому приложение может использовать это для 
        перенаправления после входа в систему.'''
        next_page = request.args.get('next')
        """
        Чтобы определить, является ли URL относительным или абсолютным, 
        я анализирую его с помощью функции url_parse() Werkzeug, 
        а затем проверяю, установлен ли компонент netloc или нет."""
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


