from project import db, create_app, models

if __name__ == '__main__':
    with create_app().app_context():
        db.create_all()
