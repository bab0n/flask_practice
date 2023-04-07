from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # primary keys are required by SQLAlchemy
    login = db.Column(db.Text)
    password = db.Column(db.Text)
    status = db.Column(db.Text)


class Reply(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sender = db.Column(db.Integer)
    content = db.Column(db.Text)
    status = db.Column(db.Text)
    doer = db.Column(db.Integer)
    date = db.Column(db.Text)


class Log(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    reply = db.Column(db.Integer)
    worker = db.Column(db.Text)
    action = db.Column(db.Text)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    reason = db.Column(db.Text)
