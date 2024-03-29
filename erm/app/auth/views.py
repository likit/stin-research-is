from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required, logout_user, login_user, current_user
from app.auth.forms import RegisterForm, LoginForm, NewUserForm, PasswordChangeForm, PasswordResetForm
from app.main.models import User
from app.researcher.models import Profile
from app import db, login_manager, superuser
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
                new_profile = Profile()
                new_profile.user = new_user
                db.session.add(new_user)
                db.session.commit()
                flash('Your email has been registered successfully. Please wait for your account to be verified and activated.', 'is-success')
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
            if user and user.is_activated:
                if user.check_password(password):
                    login_user(user)
                    if current_user.is_authenticated:
                        flash('You have been signed in.', 'success')
                    else:
                        flash('You have not been activated.'
                              ' Please wait for the admin to verify your account.',
                              'warning')
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
@superuser
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


@auth.route('/users/edit-password', methods=['GET', 'POST'])
@login_required
def edit_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if current_user.check_password(request.form.get('curr_password')):
            if current_user.check_password(request.form.get('new_password')):
                flash('A new password is the same as the current password.', 'warning')
                return render_template('auth/edit_password.html', form=form)
            else:
                current_user.password = request.form.get('new_password')
                db.session.add(current_user)
                db.session.commit()
                flash('New password has been set.', 'success')
                return redirect(url_for('researcher.show_profile', user_id=current_user.id))
        else:
            flash('Invalid current password.', 'danger')
            return render_template('auth/edit_password.html', form=form)
    else:
        print(form)

    return render_template('auth/edit_password.html', form=form)


@auth.route('/users/<int:user_id>/edit-password', methods=['GET', 'POST'])
@superuser
@login_required
def reset_password(user_id):
    user = User.query.get(user_id)
    form = PasswordResetForm()
    if form.validate_on_submit():
        current_user.password = request.form.get('new_password')
        db.session.add(current_user)
        db.session.commit()
        flash('Password has been reset.', 'success')
        return redirect(url_for('webadmin.list_users', user_id=current_user.id))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/users/<int:user_id>/deactivate')
@superuser
@login_required
def deactivate_user(user_id):
    confirmed = request.args.get('confirmed')
    if confirmed is None:
        return render_template('auth/deactivate_confirm.html', user_id=user_id)
    elif confirmed == 'yes':
        user = User.query.get(user_id)
        user.is_activated = not user.is_activated
        db.session.add(user)
        db.session.commit()
        status = 'activated' if user.is_active else 'deactivated'
        flash('User has been {}'.format(status), 'success')
    return redirect(url_for('webadmin.list_users'))