from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,SubmitField,BooleanField,ValidationError
from wtforms.validators import Required,Email
from ..models import Subscriber
import email_validator


class PostForm(FlaskForm):
    title = StringField('Post title',validators=[Required()])
    text = TextAreaField('Your post', validators=[Required()],render_kw={'class': 'form-control', 'rows': 10})
    category = SelectField('Category', validators=[Required()], choices=[('frontend','Frontend'),('backend','Backend'),('mobile','Mobile'),('fullstack','Fullstack'),('devOps','DevOps')])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = StringField('Comment',validators = [Required()])
    submit = SubmitField('Post')

class SubscribeForm(FlaskForm):
    email = StringField('Your Email',validators=[Required(),Email()])
    submit = SubmitField('Subscribe')

    def validate_email(self,data_field):
        if Subscriber.query.filter_by(email =data_field.data).first():
            raise ValidationError("You've already subscribed.")

class UnsubscribeForm(FlaskForm):
    email = StringField('Your Email',validators=[Required(),Email()])
    submit = SubmitField('Unsubscribe')

    def validate_email(self,data_field):
        if Subscriber.query.filter_by(email =data_field.data).first() == None:
            raise ValidationError("You are not subscribed.")