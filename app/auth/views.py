from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from app import db
from .forms import LoginForm, RegistrationForm

# Login function
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # Retrieving value of the next parameter
            next = request.args.get('next')
            # This condition checks if the 'next' parameter is not present or does not start with a forward slash (/)
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

# register user
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now login.')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

# Log out function
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))