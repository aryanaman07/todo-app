from flask import Blueprint, render_template, request, url_for, flash, redirect
from app import db
from app.models import User
from sqlalchemy import or_
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # if already logged in, go to tasks
    if current_user.is_authenticated:
        return redirect(url_for('tasks.view_tasks'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # check if already register
        existing_user = User.query.filter(or_(User.username == username, User.email == email)).first()
        if existing_user:
            flash('Username or email already existed!', 'danger')
            return redirect(url_for('auth.register'))

        # if not creating new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please Log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.view_tasks'))

    if request.method == 'POST':
        credential = request.form.get('username')  # username or email
        password = request.form.get('password')

        # allow login by username or email
        user = User.query.filter(or_(User.username == credential, User.email == credential)).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login Successfully!', 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!', 'info')
    return redirect(url_for('auth.login'))