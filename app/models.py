from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import db
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


class Quote:
    def __init__(self,author,quote):
        self.author = author
        self.quote = quote


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)    
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'{self.username}'


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key = True)
    title=db.Column(db.String)
    text=db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)    
    category = db.Column(db.String)    

    def save_post(self):
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return f'{self.title}'