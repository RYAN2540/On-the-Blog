from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,logout_user,login_required
from . import auth
from ..models import Admin
from .forms import RegistrationForm,LoginForm
from .. import db

@auth.route('/login',methods=['GET', 'POST'])
def login():
    if len(Admin.query.all())==0:
        return redirect(url_for('auth.register'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        admin = Admin.query.filter_by(email = login_form.email.data).first()
        if admin is not None and admin.verify_password(login_form.password.data):
            login_user(admin,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or password')

    title = "Admin login"
    return render_template('auth/login.html',login_form = login_form,title=title)


@auth.route('/register',methods = ["GET","POST"])
def register():
    if len(Admin.query.all())>0:
        return redirect(url_for('auth.login'))

    form = RegistrationForm()
    if form.validate_on_submit():
        admin = Admin(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('auth.login'))
    title = "Admin registration"
    return render_template('auth/register.html',registration_form = form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))