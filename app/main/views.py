from flask import render_template,request,redirect,url_for
from flask_login import login_required
from . import main
from ..requests import get_quote
from .forms import PostForm,CommentForm,SubscribeForm,UnsubscribeForm
from ..models import Post,Comment,Subscriber
from .. import db
from ..email import mail_message


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

        mail_list=[]
        subscribers=Subscriber.query.order_by(Subscriber.id.desc())
        for sub in subscribers:
            mail_list.append(sub.email)

        mail_message("New post on On the Blog","email/new_post",mail_list,this_post=this_post)

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


@main.route('/comment/delete/<post_id>/<comment_id>',methods = ['GET','POST'])
@login_required
def delete_comment(comment_id, post_id):
    comment= Comment.query.filter_by(id = comment_id).first() 
    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('.blog_post', post_id=post_id))



@main.route('/subscribe',methods = ['GET','POST'])
def subscribe():
    form=SubscribeForm()

    if form.validate_on_submit():
        new_email = form.email.data             

        # Updated subscriber instance
        this_subscriber = Subscriber(email=new_email)

        # save subscriber method
        this_subscriber.save_subscriber()

        mail_list=[]
        mail_list.append(new_email)

        mail_message("Your subscription to On the Blog.","email/new_subscriber",mail_list)

        return redirect(url_for('.index'))   

    title = 'Subscribe'
    return render_template('subscribe.html',title = title, subscription_form=form)


@main.route('/unsubscribe',methods = ['GET','POST'])
def unsubscribe():
    form=UnsubscribeForm()

    if form.validate_on_submit():
        new_email = form.email.data             

        unsubscriber= Subscriber.query.filter_by(email = new_email).first() 
        db.session.delete(unsubscriber)
        db.session.commit()

        mail_list=[]
        mail_list.append(new_email)

        mail_message("You've unsubscribed from codescripts.","email/bye",mail_list)

        return redirect(url_for('.index'))   

    title = 'Unsubscribe'
    return render_template('unsubscribe.html',title = title, unsubscribe_form=form)


