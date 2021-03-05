from flask import render_template,request,redirect,url_for
from flask_login import login_required
from . import main
from ..requests import get_quote
from .forms import PostForm
from ..models import Post


@main.route('/')
def index():
    quote=get_quote()

    return render_template('index.html', quote=quote)


@main.route('/admin')
@login_required
def admin(): 
    form=PostForm()        
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        category = form.category.data

        # Updated post instance
        this_post = Post(title=title, text=text, category=category)

        # save post method
        this_post.save_post()
        return redirect(url_for('.admin'))

    title = 'Admin Page'

    return render_template('admin.html', title=title, post_form=form)    

