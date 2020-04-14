from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_paginate import Pagination, get_page_parameter
from datetime import datetime
from werkzeug.urls import url_parse
from flask_login import login_required, current_user, login_user, logout_user
from app.vendor.web.forms import LoginForm, RegistrationForm, SoftwareForm
from app.vendor.models.user import User
from app.vendor.models.software import Software
from app.vendor.dao.user import UserDao
from app.vendor.dao.software import SoftwareDao

vendor_app = Blueprint('vendor_app', __name__)


@vendor_app.route('/')
@vendor_app.route('/index')
def index():
    return render_template('index.html', title='Home')


@vendor_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserDao.get_by_email(form.email.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('vendor_app.index'))
        user.last_login_date = datetime.utcnow
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('vendor_app.dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@vendor_app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('vendor_app.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.email = form.email.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.set_password(form.password.data)
        UserDao.save_user(user)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('vendor_app.dashboard'))
    return render_template('register.html', title='Register', form=form)


@vendor_app.route('/dashboard')
@login_required
def dashboard():

    per_page = 3
    page = request.args.get(get_page_parameter(), type=int, default=1)
    offset = (page - 1) * per_page

    all_software = SoftwareDao.get_software_pagination()
    softwares_for_render = all_software.limit(per_page).offset(offset)

    pagination = Pagination(page=page,
                            total=all_software.count(),
                            record_name='Software',
                            per_page=3,
                            css_framework='bootstrap4')

    # get the software
    all_software = SoftwareDao.get_all()
    return render_template('dashboard.html',
                           title='Dashboard',
                           all_software=softwares_for_render,
                           pagination=pagination)


@vendor_app.route('/software', methods=['GET', 'POST'])
@login_required
def software():
    form = SoftwareForm()
    if form.validate_on_submit():
        software = Software()
        software.software_name = form.software_name.data
        software.provider = form.provider.data
        software.department = form.department.data
        software.budget_owner = form.budget_owner.data
        software.software_owner = form.software_owner.data
        software.expiration_date = form.expiration_date.data
        software.payment_method = form.payment_method.data
        SoftwareDao.save_software(software)
        return redirect(url_for('vendor_app.dashboard'))
    return render_template('software.html', title='Add Software', form=form)


@vendor_app.route('/editsoftware/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_software(id):
    software = SoftwareDao.get_by_id(id)

    if software:
        form = SoftwareForm(formdata=request.form, obj=software)
        if request.method == 'POST' and form.validate():
            software.software_name = form.software_name.data
            software.provider = form.provider.data
            software.budget_owner = form.budget_owner.data
            software.department = form.department.data
            software.expiration_date = form.expiration_date.data
            software.payment_method = form.payment_method.data
            software.last_update_date = datetime.utcnow()
            SoftwareDao.save_software(software)
            return redirect(url_for('vendor_app.dashboard'))
        return render_template('software.html', title='Update Software', form=form)


@vendor_app.route('/software/delete/<int:id>')
@login_required
def delete_software(id):
    SoftwareDao.delete(id)
    return redirect(url_for('vendor_app.dashboard'))


@vendor_app.route('/software/<int:id>')
@login_required
def get_software(id):
    software = SoftwareDao.get_by_id(id)

    if software:
        form = SoftwareForm(formdata=request.form, obj=software)
        return render_template('software_detail.html', title='View Software', software=software)


@vendor_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('vendor_app.index'))
