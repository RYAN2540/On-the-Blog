from flask import render_template,request,redirect,url_for
from flask_login import login_required
from . import main
from ..requests import get_quote
# from .forms import ReviewForm
# from ..models import Review


@main.route('/')
def index():
    quote=get_quote()

    return render_template('index.html', quote=quote)


@main.route('/admin')
@login_required
def admin():    

    return render_template('admin.html')
