from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SubmitField
from wtforms.validators import Required

class PostForm(FlaskForm):
    title = StringField('Post title',validators=[Required()])
    text = TextAreaField('Your post', validators=[Required()],render_kw={'class': 'form-control', 'rows': 20})
    category = SubmitField('Category', validators=[Required()], choices=[('frontend','Frontend'),('backend','Backend'),('mobile','Mobile'),('fullstack','Fullstack'),('devOps','DevOps')])
    submit = SubmitField('Post')