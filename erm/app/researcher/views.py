from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required
from app.main.models import User
from app.researcher.models import Profile, Education
from app.researcher.forms import ProfileForm, EducationForm
from app import db
from . import researcher_bp as researcher


@researcher.route('/profile/<int:user_id>')
@login_required
def show_profile(user_id):
    user = User.query.get(user_id)
    if not user.profile:
        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()
    return render_template('researcher/profile.html', user=user)


@researcher.route('/profile/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    user = User.query.get(user_id)
    form = ProfileForm(obj=user.profile, programs=user.profile.program)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(user.profile)
            user.profile.program = form.programs.data
            db.session.add(user.profile)
            db.session.commit()
            flash('Data has been saved.', 'success')
            return redirect(url_for('researcher.show_profile', user_id=user.id))
        else:
            flash('Errors occurred.', 'danger')
            return redirect(url_for('researcher.show_profile', user_id=user.id))
    return render_template('researcher/profile_edit.html', form=form)



@researcher.route('/profile/<int:profile_id>/education/new', methods=['GET', 'POST'])
@login_required
def add_education(profile_id):
    profile = Profile.query.get(profile_id)
    form = EducationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_edu = Education()
            new_edu.profile = profile
            form.populate_obj(new_edu)
            db.session.add(new_edu)
            db.session.commit()
            flash('New record has been added.', 'success')
        else:
            flash('Error occurred.', 'danger')
        return redirect(url_for('researcher.show_profile', user_id=profile.user_id))

    return render_template('researcher/education_add.html', form=form)


@researcher.route('/profile/education/<int:edid>/edit', methods=['GET', 'POST'])
@login_required
def edit_education(edid):
    edu = Education.query.get(edid)
    form = EducationForm(obj=edu, degree=edu.degree)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(edu)
            db.session.add(edu)
            db.session.commit()
            flash('Record has been edited.', 'success')
        else:
            flash('Error occurred.', 'danger')
        return redirect(url_for('researcher.show_profile', user_id=edu.profile.user_id))

    return render_template('researcher/education_add.html', form=form)
