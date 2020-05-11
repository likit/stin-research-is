import os
import arrow
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from . import project_bp as project
from .models import *
from .forms import *
from app.main.models import User
import requests
from pydrive.auth import ServiceAccountCredentials, GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
keyfile_dict = requests.get(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')).json()
scopes = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, scopes)
drive = GoogleDrive(gauth)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def make_project_archive(project):
    """Create an archive of a project.
    :param project: a project model
    :return: archive model
    """

    archive = ProjectRecordArchive(
        project_record_id=project.id,
        archived_at=arrow.now(tz='Asia/Bangkok').datetime,
        title_th=project.title_th,
        subtitle_th=project.subtitle_th,
        title_en=project.title_en,
        subtitle_en=project.subtitle_en,
        objective=project.objective,
        method=project.method,
        intro=project.intro,
        status=project.status,
        prospected_journals=project.prospected_journals,
        use_applications=project.use_applications,
        created_at=project.created_at,
        updated_at=project.updated_at,
        creator_id=project.creator_id
    )
    members = []
    for member in project.members:
        mem = {
            'role': member.role,
            'fullname_th': member.user.profile.fullname_th,
            'fullname_en': member.user.profile.fullname_en,
            'title_th': member.user.profile.title_th,
            'title_en': member.user.profile.title_en,
        }
        members.append(mem)
    figures = []
    for figure in project.figures:
        fig = {
            'title': figure.title,
            'desc': figure.desc,
            'fignum': figure.fignum,
            'url': figure.url,
        }
        figures.append(fig)
    milestones = []
    for milestone in project.milestones:
        mst = {
            'deadline': milestone.deadline,
            'goal': milestone.goal,
            'status': milestone.status,
            'detail': milestone.detail
        }
        milestones.append(mst)
    archive.members = members
    archive.figures = figures
    archive.milestones = milestones
    return archive


@project.route('/')
def list_projects():
    projects = ProjectRecord.query.all()
    return render_template('project/index.html', projects=projects)


@project.route('/user/<int:user_id>')
@login_required
def list_created_projects(user_id):
    user = User.query.get(user_id)
    projects = user.projects
    return render_template('project/created_projects.html', projects=projects)


@project.route('/detail/<int:project_id>')
def display_project(project_id):
    project = ProjectRecord.query.get(project_id)
    return render_template('project/detail.html', project=project)


@project.route('/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = ProjectRecord.query.get(project_id)
    form = ProjectRecordForm(obj=project)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(project)
            project.updated_at = arrow.now(tz='Asia/Bangkok').datetime
            db.session.add(project)
            db.session.commit()
            flash('Data have been updated.', 'success')
        else:
            flash('Error occurred.', 'danger')
        return redirect(url_for('project.display_project', project_id=project.id))
    return render_template('project/project_edit.html', form=form)


@project.route('/add', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectRecordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_proj = ProjectRecord()
            form.populate_obj(new_proj)
            new_proj.creator = current_user
            current_datetime = arrow.now(tz='Asia/Bangkok').datetime
            new_proj.created_at = current_datetime
            new_proj.updated_at = current_datetime
            new_proj.status = 'draft'
            db.session.add(new_proj)
            db.session.commit()
            flash('Data have been updated.', 'success')
        else:
            flash('Error occurred.', 'danger')
        return redirect(url_for('project.display_project', project_id=new_proj.id))
    return render_template('project/project_edit.html', form=form)

@project.route('/<int:project_id>/member/add', methods=['GET', 'POST'])
@login_required
def add_member(project_id):
    form = ProjectMemberForm()
    if form.validate_on_submit():
        new_member = ProjectMember(project_id=project_id)
        form.populate_obj(new_member)
        new_member.user = form.users.data
        db.session.add(new_member)
        db.session.commit()
        flash('New member has been added.', 'success')
        return redirect(url_for('project.display_project', project_id=project_id))
    return render_template('project/member_add.html', form=form)


@project.route('/<int:project_id>/member/<int:member_id>/remove', methods=['GET', 'POST'])
@login_required
def remove_member(project_id, member_id):
    member = ProjectMember.query.get(member_id)
    db.session.delete(member)
    db.session.commit()
    return redirect(url_for('project.display_project', project_id=project_id))


@project.route('/<int:project_id>/application/new', methods=['GET', 'POST'])
@login_required
def add_application(project_id):
    project = ProjectRecord.query.get(project_id)
    form = ApplicationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_app = Application()
            form.populate_obj(new_app)
            new_app.project = project
            db.session.add(new_app)
            db.session.commit()
            flash('Application has been recorded.', 'success')
        else:
            flash('Error occurred.', 'danger')
        return redirect(url_for('project.display_project', project_id=project.id))
    return render_template('project/application_add.html', form=form)


@project.route('/application/<int:app_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_application(app_id):
    app = Application.query.get(app_id)
    form = ApplicationForm(obj=app)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(app)
            db.session.add(app)
            db.session.commit()
            flash('Application has been updated.', 'success')
        else:
            flash('Error occurred.', 'danger')
        return redirect(url_for('project.display_project', project_id=app.project.id))
    return render_template('project/application_add.html', form=form)


@project.route('/application/<int:app_id>/remove', methods=['GET', 'POST'])
@login_required
def remove_application(app_id):
    application = Application.query.get(app_id)
    project_id = application.project_id
    try:
        db.session.delete(application)
        db.session.commit()
    except:
        flash('Error occurred.', 'danger')
    else:
        flash('Application has been removed.', 'success')
    return redirect(url_for('project.display_project', project_id=project_id))


@project.route('/<int:project_id>/figure/add', methods=['GET', 'POST'])
@login_required
def add_figure(project_id):
    form = ProjectFigureForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if 'file' not in request.files:
                flash('No file uploaded.', 'warning')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file.', 'warning')
                return redirect(request.url)
            else:
                filename = secure_filename(file.filename)
                file.save(filename)
                file_drive = drive.CreateFile({'title': filename})
                file_drive.SetContentFile(filename)
                file_drive.Upload()
                permission = file_drive.InsertPermission({'type': 'anyone',
                                                          'value': 'anyone',
                                                          'role': 'reader'})
            new_figure = ProjectFigure()
            form.populate_obj(new_figure)
            new_figure.project_id = project_id
            new_figure.url = file_drive['id']
            db.session.add(new_figure)
            db.session.commit()
            return redirect(url_for('project.display_project', project_id=project_id))
    project = ProjectRecord.query.get(project_id)
    return render_template('project/figure_add.html', project=project, form=form)


@project.route('/figure/<int:figure_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_figure(figure_id):
    figure = ProjectFigure.query.get(figure_id)
    form = ProjectFigureForm(obj=figure)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(figure)
            db.session.add(figure)
            db.session.commit()
            return redirect(url_for('project.display_project', project_id=figure.project.id))
    return render_template('project/figure_add.html', form=form)


@project.route('/figure/<int:figure_id>/remove', methods=['GET', 'POST'])
@login_required
def remove_figure(figure_id):
    figure = ProjectFigure.query.get(figure_id)
    try:
        db.session.delete(figure)
        db.session.commit()
    except:
        flash('Error occurred.', 'danger')
    else:
        flash('Figure has been removed.', 'success')
    return redirect(request.referrer)


@project.route('/<int:project_id>/submit', methods=['GET'])
@login_required
def submit_project(project_id):
    project = ProjectRecord.query.get(project_id)
    project.status = 'submitted'
    project.updated_at = arrow.now(tz='Asia/Bangkok').datetime
    project.submitted_at = arrow.now(tz='Asia/Bangkok').datetime
    db.session.add(project)
    archive = make_project_archive(project)
    db.session.add(archive)
    db.session.commit()
    flash('Project has been submitted for a review.', 'success')
    return redirect(url_for('project.display_project', project_id=project.id))


@project.route('/<int:project_id>/ethic/add/confirm', methods=['GET', 'POST'])
@login_required
def confirm_add_ethic(project_id):
    project = ProjectRecord.query.get(project_id)
    return render_template('project/ethic_add.html', project=project)


@project.route('/<int:project_id>/ethic/add/confirmed', methods=['GET'])
@login_required
def add_ethic_request(project_id):
    project = ProjectRecord.query.get(project_id)
    if project.status != 'full':
        flash('The project must be reviewed by the center '
              'before submmiting for an ethic approval', 'warning')
        return redirect(request.referrer)

    ethic = ProjectEthicRecord(project_id=project_id,
                               submitted_at=arrow.now(tz='Asia/Bangkok').datetime,
                               status='submitted')
    archive = make_project_archive(project)
    project.updated_at = arrow.now(tz='Asia/Bangkok').datetime
    db.session.add(ethic)
    db.session.add(archive)
    db.session.add(project)
    db.session.commit()
    return redirect(url_for('project.display_project', project_id=project.id))


@project.route('/archive/<int:archive_id>', methods=['GET'])
@login_required
def view_archive(archive_id):
    ar = ProjectRecordArchive.query.get(archive_id)
    return render_template('project/archieve_detail.html', project=ar)


@project.route('/<int:project_id>/milestone/add', methods=['GET', 'POST'])
@login_required
def add_milestone(project_id):
    project = ProjectRecord.query.get(project_id)
    form = ProjectMilestoneForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_milestone = ProjectMilestone()
            form.populate_obj(new_milestone)
            new_milestone.project_id = project_id
            db.session.add(new_milestone)
            db.session.commit()
            flash('New milestone added.')
            return redirect(url_for('project.display_project', project_id=project_id))
    return render_template('project/milestone_add.html', project=project, form=form)


@project.route('/admin/ethics', methods=['GET', 'POST'])
@login_required
def list_ethics(project_id):
    ethics = ProjectEthicRecord.query.get(project_id)
    return 'Hello'


@project.route('/journals/add', methods=['GET', 'POST'])
def add_journal():
    form = ProjectJournalForm()
    project_id = request.args.get('project_id')
    if request.method == 'POST':
        if form.validate_on_submit():
            new_journal = ProjectPublicationJournal()
            form.populate_obj(new_journal)
            db.session.add(new_journal)
            db.session.commit()
            flash('New journal added.', 'success')
        else:
            flash(form.errors, 'danger')
        if project_id:
            return redirect(url_for('project.add_pub', project_id=project_id))
    return render_template('project/journal_add.html', form=form, project_id=project_id)


@project.route('/projects/<int:project_id>/pubs/<int:pub_id>/authors/add', methods=['GET', 'POST'])
def add_pub_author(project_id, pub_id):
    form = ProjectPublicationAuthorForm()
    pub = ProjectPublication.query.get(pub_id)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_author = ProjectPublicationAuthor()
            form.populate_obj(new_author)
            new_author.pub = pub
            new_author.user = form.users.data
            db.session.add(new_author)
            db.session.commit()
            flash('New author has been added.', 'success')
            return redirect(url_for('project.edit_pub_authors', pub_id=pub_id, project_id=project_id))
    return render_template('webadmin/pub_author_add.html', form=form)


@project.route('/<int:project_id>/pubs/add', methods=['GET', 'POST'])
@login_required
def add_pub(project_id):
    form = ProjectPublicationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_pub = ProjectPublication()
            form.populate_obj(new_pub)
            new_pub.project_id = project_id
            new_pub.journal = form.journals.data
            db.session.add(new_pub)
            db.session.commit()
            flash('New publication added.')
            return redirect(url_for('project.edit_pub_authors',
                                    project_id=project_id, pub_id=new_pub.id))
    return render_template('webadmin/pub_add.html', form=form, project_id=project_id)


@project.route('projects/<int:project_id>/pubs/<int:pub_id>/edit', methods=['GET', 'POST'])
def edit_pub(project_id, pub_id):
    pub = ProjectPublication.query.get(pub_id)
    form = ProjectPublicationForm(obj=pub)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(pub)
            db.session.add(pub)
            db.session.commit()
            flash('Data have been saved.', 'success')
            return redirect(url_for('project.display_project', project_id=project_id))
        else:
            flash(form.errors, 'danger')
    return render_template('webadmin/pub_edit.html', form=form, pub=pub, project_id=project_id)


@project.route('projects/<int:project_id>/pubs/<int:pub_id>/authors/edit', methods=['GET', 'POST'])
def edit_pub_authors(project_id, pub_id):
    pub = ProjectPublication.query.get(pub_id)
    return render_template('webadmin/pub_author_edit.html', pub=pub, project_id=project_id)



@project.route('/projects/<int:project_id>/pubs/<int:pub_id>/authors/<int:author_id>/remove')
def remove_pub_author(project_id, pub_id, author_id):
    author = ProjectPublicationAuthor.query.get(author_id)
    if author:
        db.session.delete(author)
        db.session.commit()
        flash('Author has been deleted from publication', 'success')
    else:
        flash('The author with that ID was not found.', 'danger',)
    return redirect(url_for('project.edit_pub_authors', project_id=project_id, pub_id=pub_id))


@project.route('/<int:project_id>/pubs/<int:pub_id>/support/language/add', methods=['GET', 'POST'])
@login_required
def add_lang_support(project_id, pub_id):
    form = ProjectLanguageEditSupportForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_support = ProjectLanguageEditingSupport()
            form.populate_obj(new_support)
            new_support.qualification = '|'.join(form.qualification_select.data)
            new_support.criteria = '|'.join(form.criteria_select.data)
            new_support.docs = '|'.join(form.docs_select.data)
            new_support.request = '|'.join(form.request_select.data)
            new_support.pub_id = pub_id
            new_support.submitted_at = arrow.now(tz='Asia/Bangkok').datetime,
            db.session.add(new_support)
            db.session.commit()
            flash('New language edit request added.')
            return redirect(url_for('project.display_project', project_id=project_id))
    return render_template('project/lang_support_add.html', project=project, form=form)


@project.route('/<int:project_id>/pubs/<int:pub_id>/support/language/<int:record_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lang_support(project_id, pub_id, record_id):
    record = ProjectLanguageEditingSupport.query.get(record_id)
    form = ProjectLanguageEditSupportForm(obj=record)
    criteria = record.criteria.split('|')
    qualification = record.qualification.split('|')
    docs = record.docs.split('|')
    request_data = record.request.split('|')
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(record)
            record.qualification = '|'.join(form.qualification_select.data)
            record.criteria = '|'.join(form.criteria_select.data)
            record.docs = '|'.join(form.docs_select.data)
            record.request = '|'.join(form.request_select.data)
            record.pub_id = pub_id
            record.edited_at = arrow.now(tz='Asia/Bangkok').datetime,
            db.session.add(record)
            db.session.commit()
            flash('New language edit request edited.')
            return redirect(url_for('project.display_project', project_id=project_id))
    return render_template('project/lang_support_edit.html',
                           project=project, form=form,
                           docs=docs, request_data=request_data,
                           qualification=qualification, criteria=criteria)


@project.route('/<int:project_id>/pubs/<int:pub_id>/support/reward/add', methods=['GET', 'POST'])
@login_required
def add_pub_reward(project_id, pub_id):
    pub = ProjectPublication.query.get(pub_id)
    form = ProjectPublishedRewardForm()
    return render_template('project/reward_add.html',
                           pub=pub, project_id=project_id, form=form)
