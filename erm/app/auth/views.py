from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required, logout_user, login_user, current_user
from app.auth.forms import RegisterForm, LoginForm, NewUserForm
from app.main.models import User
from app.researcher.models import Profile
from app import db, login_manager
from . import auth_bp as auth


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.route('register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form.get('email')
            password = request.form.get('password')
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('The user with this email account has already been registered.', 'is-danger')
                return redirect(request.referrer)
            else:
                new_user = User(email, password)
                db.session.add(new_user)
                db.session.commit()
                flash('Your email has been registered successfully.', 'is-success')
                return redirect(request.referrer)
        else:
            for field, msg in form.errors.items():
                flash('{}: {}'.format(
                    ' '.join([f.title() for f in field.split('_')]), ', '.join(msg)), 'is-danger')
            return redirect(request.referrer)

    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user.is_authenticated:
                flash('You have been already logged in.', 'success')
                return redirect(url_for('main.index'))

            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user:
                if user.check_password(password):
                    login_user(user)
                    flash('You have been signed in.', 'success')
                    return redirect(url_for('main.index'))
                else:
                    flash('Password is incorrect. Please try again.', 'danger')
            else:
                flash('The email has not been registered in this system.', 'warning')
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if not current_user.is_authenticated:
        flash('You were already signed out.', 'success')
        return redirect(request.referrer)
    else:
        logout_user()
        flash('You have been signed out.', 'success')
        return redirect(url_for('main.index'))


@auth.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    form = NewUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form.get('email')
            if email:
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    flash('The user with this email already exists.', 'danger')
                else:
                    firstname = request.form.get('firstname')
                    lastname = request.form.get('lastname')
                    password = request.form.get('password')
                    new_user = User(email, password)
                    new_profile = Profile()
                    new_profile.user = new_user
                    new_profile.firstname_th = firstname
                    new_profile.lastname_th = lastname
                    db.session.add(new_user)
                    db.session.add(new_profile)
                    db.session.commit()
                    flash('The user has been added.', 'success')
                    return redirect(url_for('webadmin.list_users'))
        else:
            flash(form.errors, 'danger')
    return render_template('auth/new_user.html', form=form)
