from . import db
from flask_login import UserMixin

# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=db.func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #relationship with user table one-to-many. that is one user to many notes

class User(db.Model, UserMixin): #usermixin only for user to inherit
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # notes = db.relationship('Note') #relationship with note table one-to-many. that is one user to many notes

class SUser(db.Model, UserMixin): #usermixin only for user to inherit
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # notes = db.relationship('Note') #relationship with note table one-to-many. that is one user to many notes

class AUser(db.Model, UserMixin): #usermixin only for user to inherit
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))