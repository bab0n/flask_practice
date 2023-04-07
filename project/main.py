from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, current_user, login_required, logout_user
from . import db
from .models import User

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if len(current_user.__dict__) == 4:
        return redirect(url_for('auth.lk'))
    return render_template('index.html')


@main.route('/profile')
def profile():
    return 'Profile'
