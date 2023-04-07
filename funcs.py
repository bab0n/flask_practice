from project.models import User
from project import db


def add_user(login, password):
    new_user = User(login=login, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user.id


add_user('Саня ебать', 'pas')
