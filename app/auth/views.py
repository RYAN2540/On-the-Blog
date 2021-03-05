from flask import render_template,redirect,url_for
from . import auth
from ..models import Admin
from .forms import RegistrationForm
from .. import db

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        admin = Admin(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('auth.login'))
        title = "Admin login"
    return render_template('auth/register.html',registration_form = form)