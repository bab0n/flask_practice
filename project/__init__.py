import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
UPLOAD_FOLDER = 'C:\\Users\\bab0n\\Desktop\\lear\\replys'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


db = SQLAlchemy()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)

    # схема для авторизованных юзеров
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # схема для неавторизованных юзеров
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


# @app.route('/f', methods=['POST'])
# def f():
#     if len(request.form['text']) < 0:
#         return render_template('sendet.html', state='Заявка не содержит текста')
#     file = request.files['file']
#     if file and (not allowed_file(file.filename)):
#         return render_template('sendet.html', state='Недопустимое расширение файла')
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     return render_template('sendet.html', state='Заявка успешно отправлена')


# @app.route('/')
# def index():
#     return render_template('index.html')


if __name__ == '__main__':
    create_app().run(debug=True)
