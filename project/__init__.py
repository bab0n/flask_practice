import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
UPLOAD_FOLDER = 'C:\\Users\\bab0n\\Desktop\\lear\\replys'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ADMIN_PASSWORD = 'admin1'

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # поскольку user_id является первичным ключом нашей таблицы пользователей, используйте его в запросе для пользователя
        return User.query.get(int(user_id))

    # схема для авторизованных юзеров
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # схема для неавторизованных юзеров
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
