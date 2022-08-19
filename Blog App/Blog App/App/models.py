from email.policy import default
from App import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True) 
    password = db.Column(db.String(50), nullable = False)
    profile_filename = db.Column(db.String(50), default = 'profile pic.jpg')
    posts = db.relationship('Post')


class Post(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    post_data = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


