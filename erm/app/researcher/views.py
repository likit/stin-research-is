import os
import requests
import arrow
from flask import render_template, flash, request, redirect, url_for, session
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.main.models import User
from app.researcher.models import Profile, Education, IntlConferenceSupport
from app.researcher.forms import ProfileForm, EducationForm, IntlConferenceSupportForm
from app import db
from . import researcher_bp as researcher
from app.project.models import (ProjectPublication,
                                ProjectPublicationAuthor,
                                ProjectPublicationJournal)
from app.project.forms import (ProjectPublicationForm,
                               ProjectJournalForm,
                               ProjectPublicationAuthorForm)
from pydrive.auth import ServiceAccountCredentials, GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
keyfile_dict = requests.get(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')).json()
scopes = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, scopes)
drive = GoogleDrive(gauth)


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
            photo_file = form.photo_upload.data
            if photo_file:
                filename = secure_filename(photo_file.filename)
                photo_file.save(filename)
                file_drive = drive.CreateFile({'title': filename})
                file_drive.SetContentFile(filename)
                file_drive.Upload()
                permission = file_drive.InsertPermission({'type': 'anyone',
                                                          'value': 'anyone',
                                                          'role': 'reader'})
                user.profile.photo_url = file_drive['id']
                print(user.profile.photo_url)
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


@researcher.route('/profile/education/<int:edid>/remove', methods=['GET', 'POST'])
@login_required
def remove_education(edid):
    edu = Education.query.get(edid)
    user_id = edu.profile.user_id
    try:
        db.session.delete(edu)
        db.session.commit()
    except:
        flash('Error occurred.')
    else:
        flash('Record has been removed', 'success')
    return redirect(url_for('researcher.show_profile', user_id=user_id))


@researcher.route('/journals/add', methods=['GET', 'POST'])
@login_required
def add_journal():
    dest = request.args.get('next')
    pub_id = request.args.get('pub_id')
    form = ProjectJournalForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_journal = ProjectPublicationJournal()
            form.populate_obj(new_journal)
            db.session.add(new_journal)
            db.session.commit()
            flash('New journal has been added.', 'success')
            return redirect(url_for(dest, pub_id=pub_id))
        else:
            flash(form.errors, 'danger')
    return render_template('researcher/journal_add.html', form=form)


@researcher.route('/pubs/add', methods=['GET', 'POST'])
@login_required
def add_pub():
    form = ProjectPublicationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_pub = ProjectPublication()
            form.populate_obj(new_pub)
            new_pub.journal = form.journals.data
            author = ProjectPublicationAuthor()
            author.user = current_user
            new_pub.authors.append(author)
            db.session.add(author)
            db.session.add(new_pub)
            db.session.commit()
            flash('New publication added.', 'success')
            return redirect(url_for('researcher.show_profile',
                                    user_id=current_user.id))
        else:
            flash('Error occurred.', 'danger')
    return render_template('researcher/pub_add.html', form=form)


@researcher.route('/pubs/<int:pub_id>')
@login_required
def show_pub(pub_id):
    pub = ProjectPublication.query.get(pub_id)
    return render_template('researcher/pub_detail.html', pub=pub)


@researcher.route('/pubs/<int:pub_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_pub(pub_id):
    pub = ProjectPublication.query.get(pub_id)
    form = ProjectPublicationForm(obj=pub)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(pub)
            db.session.add(pub)
            db.session.commit()
            flash('Data have been saved.', 'success')
            return redirect(url_for('researcher.show_profile',
                                    user_id=current_user.id))
        else:
            flash(form.errors, 'danger')
    return render_template('researcher/pub_edit.html', form=form, pub=pub)


@researcher.route('/pubs/<int:pub_id>/authors/edit', methods=['GET', 'POST'])
@login_required
def edit_pub_authors(pub_id):
    dest = request.args.get('next')
    pub = ProjectPublication.query.get(pub_id)
    return render_template('researcher/pub_author_edit.html', pub=pub, dest=dest)


@researcher.route('/pubs/<int:pub_id>/authors/add', methods=['GET', 'POST'])
@login_required
def add_pub_author(pub_id):
    pub = ProjectPublication.query.get(pub_id)
    form = ProjectPublicationAuthorForm()
    dest = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            new_author = ProjectPublicationAuthor()
            form.populate_obj(new_author)
            new_author.pub = pub
            new_author.user = form.users.data
            db.session.add(new_author)
            db.session.commit()
            flash('New author has been added.', 'success')
            return redirect(url_for('researcher.edit_pub_authors',
                                    pub_id=pub_id, next=dest))
        else:
            flash(form.errors, 'danger')
    return render_template('researcher/pub_author_add.html',
                           pub=pub, form=form, dest=dest)


@researcher.route('/pubs/<int:pub_id>/authors/<int:author_id>/remove', methods=['GET', 'POST'])
@login_required
def remove_pub_author(pub_id, author_id):
    author = ProjectPublicationAuthor.query.get(author_id)
    if author:
        db.session.delete(author)
        db.session.commit()
        flash('Author has been deleted from publication', 'success')
    else:
        flash('The author with that ID was not found.', 'danger',)
    return redirect(url_for('researcher.edit_pub_authors', pub_id=pub_id))


@researcher.route('/pubs/<int:pub_id>/remove', methods=['GET', 'POST'])
@login_required
def remove_pub(pub_id):
    pub = ProjectPublication.query.get(pub_id)
    confirm = request.args.get('confirm', 'no')
    if confirm == 'yes':
        if pub:
            db.session.delete(pub)
            db.session.commit()
            flash('The publication has been removed from database.', 'success')
            return redirect(url_for('researcher.show_profile', user_id=current_user.id))
        else:
            flash('The publication does not exist.', 'danger',)
    return render_template('researcher/pub_remove.html', pub=pub)


@researcher.route('/intl-support/add', methods=['GET', 'POST'])
@login_required
def add_intl_conference_support():
    form = IntlConferenceSupportForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_support = IntlConferenceSupport()
            form.populate_obj(new_support)
            new_support.qualification = '|'.join(form.qualification_select.data)
            new_support.researcher = current_user
            new_support.submitted_at = arrow.now(tz='Asia/Bangkok').datetime,
            db.session.add(new_support)
            db.session.commit()
            flash('New request for international conference support has been added.')
            return redirect(url_for('researcher.show_profile', user_id=current_user.id))
    return render_template('researcher/intl_conference_support_add.html', form=form)
