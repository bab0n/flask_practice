from . import db


class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # primary keys are required by SQLAlchemy
    login = db.Column(db.Text)
    password = db.Column(db.Text)
