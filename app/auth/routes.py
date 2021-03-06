from flask import render_template, redirect, url_for, request, flash, make_response
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ChangePasswordRequestForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import *
from app.models import User
from app.auth.token import generate_confirmation_token, confirm_token
import datetime

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Credentials invalid. Please try again or register.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.user', username=user.username)
        return redirect(next_page)
    return render_template('auth/login.html', form=form)
    

@bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, confirmed=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('auth/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(subject, user.email, html)
        login_user(user)
        #flash('A confirmation email has been sent.')
        #return redirect(url_for('main.user', username=user.username))
        return redirect(url_for('auth.unconfirmed'))
    return render_template('auth/register.html', form=form)


@bp.route('<user_id>/change-password/', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    form = ChangePasswordRequestForm()
    user = User.query.filter_by(id=user_id).first()
    if form.validate_on_submit():        
        if not user.check_password(form.old_password.data):
            flash('Current password does not match. Password cannot be changed.')
            return redirect(url_for('auth.change_password', user_id=current_user.id))
        user.set_password(form.new_password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.user', username=current_user.username))
    return render_template('auth/password.html', form=form)

@bp.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('auth/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(subject, current_user.email, html)
    flash('A new confirmation has been sent')
    return redirect(url_for('auth.unconfirmed'))

@bp.route('/unconfirmed/')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    flash('Please confirm your account')
    return render_template('auth/unconfirmed.html')

# Password reset CHECK THIS
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/passwordreset.html', title='reset password', form=form)


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
        flash('your password has been reset')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
