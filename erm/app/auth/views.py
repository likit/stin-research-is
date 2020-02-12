from flask import request, render_template, flash, redirect, url_for
from app.auth.forms import RegisterForm, LoginForm
from app.main.models import User
from app import db
from . import auth_bp as auth


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