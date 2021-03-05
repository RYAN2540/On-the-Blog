from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,SubmitField
from wtforms.validators import Required

class PostForm(FlaskForm):
    title = StringField('Post title',validators=[Required()])
    text = TextAreaField('Your post', validators=[Required()],render_kw={'class': 'form-control', 'rows': 10})
    category = SelectField('Category', validators=[Required()], choices=[('frontend','Frontend'),('backend','Backend'),('mobile','Mobile'),('fullstack','Fullstack'),('devOps','DevOps')])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = StringField('Comment publicly.',validators = [Required()])
    submit = SubmitField('Post')