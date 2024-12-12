from flask import Blueprint, request, redirect, url_for,render_template
from flask_login import LoginManager, login_user, current_user, logout_user
from models.user import User
from controllers import users


bp = Blueprint('auth_bp', __name__, url_prefix='/auth', template_folder='templates')

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.find(id=user_id)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = (User.find(email=email))

        login_user(user)
        return redirect(url_for('users.index'))
    return render_template('login.html')

bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    redirect(url_for('index'))