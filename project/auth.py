from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename
import os
from . import db, create_app, UPLOAD_FOLDER, ADMIN_PASSWORD
from .models import User, Reply, Log
import datetime

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

auth = Blueprint('auth', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@auth.route('/f', methods=['POST'])
@login_required
def f():
    user = current_user
    if len(request.form['text']) < 1:
        return render_template('sendet.html', state='Заявка не содержит текста')
    file = request.files['file']
    if file and (not allowed_file(file.filename)):
        return render_template('sendet.html', state='Недопустимое расширение файла')
    new_rep = Reply(sender=user.id, content=request.form['text'],
                    status='New', doer=0, date=datetime.date.today().isoformat())
    db.session.add(new_rep)
    db.session.commit()

    new_log = Log(reply=new_rep.id, worker='Сайт', action='Создание',
                  old_value='', new_value=new_rep.content, reason='Создание заявки')
    db.session.add(new_log)
    db.session.commit()

    path = UPLOAD_FOLDER + f'\\{new_rep.id}'
    if not os.path.exists(path):
        os.mkdir(path)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(path, f'{new_rep.id}-{filename}'))
    return render_template('sendet.html', state='Заявка успешно отправлена')


@auth.route('/new_reply')
@login_required
def new_reply():
    return render_template('new_reply.html')


@auth.route('/about_reply')
@login_required
def about_reply():
    number = request.args.get("number")
    reply = Reply.query.filter_by(sender=current_user.id, id=number).first(
    ) if current_user.status == '#user' else Reply.query.filter_by(id=number).first()
    logs = None
    if reply:
        logs = [i for i in Log.query.filter_by(id=number).all()]
    if current_user.status == '#admin':
        return render_template('reply_view.html', logs=logs, ext='admin/adm.html')
    return render_template('reply_view.html', logs=logs, ext='lk.html')


@auth.route('/lk')
@login_required
def lk():
    user = current_user
    if user.status == '#admin':
        return render_template('admin/view.html', replys=[i for i in Reply.query.all()])
    replys = [i for i in Reply.query.filter_by(sender=user.id).all()]
    return render_template('cabinet.html', replys=replys)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('login')
    password = request.form.get('pass')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(login=login).first()

    # проверка на то что пользователь существует в базе и на совпадение пароля
    if not user or not user.password == password:
        flash('Неверный логин или пароль')
        return redirect(url_for('auth.login'))

    # если пользователь существует обращаемся к модулю логина и авторизуем его
    login_user(user, remember=remember)
    return redirect(url_for('auth.lk'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    status = request.form.get('status')
    login = request.form.get('login')
    password = request.form.get('password')
    if len(password) < 1 or len(login) < 1:
        return redirect(url_for('auth.signup'))
    # Попытка получить пользователя по логину
    user = User.query.filter_by(login=login).first()

    if user:  # если пользовтаель существует программа не даст зарегеестрироваться
        flash('Логин уже занят')
        return redirect(url_for('auth.signup'))
    if status == '#admin' and request.form.get('superpass') != ADMIN_PASSWORD:
        return redirect(url_for('auth.signup'))
    # создание экземпляра нового пользователя
    new_user = User(login=login, password=password, status=status)

    # добавление пользователя в базу
    db.session.add(new_user)
    db.session.commit()

    flash(f'Пользователь успешно создан!\nID: {new_user.id}\nЛогин: {login}\nПароль: {password}')
    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/edit_reply')
@login_required
def edit_reply():
    if current_user.status == '#user':
        return redirect(url_for('auth.lk'))
    else:
        num = request.args.get("number")
        return render_template('admin/change.html', replys=[i for i in Reply.query.filter_by(id=num).all()])


@auth.route('/edit_status')
@login_required
def edit_status():
    if current_user.status == '#user':
        return redirect(url_for('auth.lk'))
    else:
        num = request.args.get("number")
        return render_template('admin/status.html', repl_id=num)
