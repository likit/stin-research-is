from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required, logout_user, login_user, current_user
from app.auth.forms import RegisterForm, LoginForm
from app.main.models import User
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
    if form.validate_on_submit():
        if current_user.is_authenticated:
            flash('User already logged in.', 'is-success')
            return redirect(url_for('main.index'))

        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user.check_password(password):
            login_user(user)
            flash('You have been signed in.', 'is-success')
            return redirect(url_for('main.index'))
        else:
            flash('Password is incorrect. Please try again.', 'is-danger')
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    if not current_user.is_authenticated:
        flash('You were already signed out.', 'is-success')
        return redirect(request.referrer)
    else:
        logout_user()
        flash('You have been signed out.', 'is-success')
        return redirect(request.referrer)
