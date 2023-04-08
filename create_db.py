from project import db, create_app, models

if __name__ == '__main__':
    with create_app().app_context():
        db.create_all()

        # Создание стандартного админа для регистрации новых пользователей
        new_user = models.User(login='admin', password='admin123', status='#admin')
        db.session.add(new_user)
        db.session.commit()
