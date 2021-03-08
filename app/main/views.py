from flask import render_template,request,redirect,url_for
from flask_login import login_required
from . import main
from ..requests import get_quote
from .forms import PostForm,CommentForm
from ..models import Post,Comment
from .. import db


@main.route('/')
def index():
    quote=get_quote()
    blog_posts=Post.query.order_by(Post.posted.desc())

    return render_template('index.html', quote=quote, posts=blog_posts)


@main.route('/admin',methods = ['GET','POST'])
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
        return redirect(url_for('.index'))

    title = 'Admin Page'

    return render_template('admin.html', title=title, post_form=form)    


@main.route('/post/<post_id>',methods = ['GET','POST'])
def blog_post(post_id):
    post=Post.query.filter_by(id=post_id).first()
    form = CommentForm()

    if form.validate_on_submit():
        new_comment = form.comment.data             

        # Updated comment instance
        this_comment = Comment(comment_text=new_comment,post=post)

        # save comment method
        this_comment.save_comment()
        return redirect(url_for('.blog_post', post_id=post_id))


    comments=Comment.query.filter_by(post_id=post_id).order_by(Comment.posted.desc())  
    title = post.title
    return render_template('post.html',title = title, comments=comments, comment_form=form, post=post)



@main.route('/post/update/<post_id>',methods = ['GET','POST'])
@login_required
def update_blog(post_id):
    form=PostForm()
    post = Post.query.filter_by(id = post_id).first()       
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.category = form.category.data        

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.blog_post', post_id=post_id))

    title = 'Update post'

    return render_template('update_post.html', title=title, post_form=form, post=post)


@main.route('/post/delete/<post_id>',methods = ['GET','POST'])
@login_required
def delete_blog(post_id):
    post= Post.query.filter_by(id = post_id).first() 
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('.index'))





