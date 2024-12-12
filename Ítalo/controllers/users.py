from flask import render_template, Blueprint, url_for, request, flash, redirect
from models.user import User
from flask_login import LoginManager,login_required, login_user
import sqlite3


bp = Blueprint('users', __name__, url_prefix='/users',template_folder='../users/templates')

login_manager = LoginManager()

def get_connection():
    conn = sqlite3.connect('../database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

@login_manager.user_loader
def load_user(user_id):
    return User.find(id=user_id)

@bp.route('/') 
@login_required
def index():
    return render_template('users/index.html', users = User.all())

@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']

        if not email:
            flash('Email é obrigatório')
        else:
            user = User(nome=nome, email=email)
            user.save()
            #alterar para redirecionar para o blueprint de login
            return redirect(url_for('users.index'))
    
    return render_template('users/register.html')

@bp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']

        conn = get_connection()

        user = conn.execute('SELECT * FROM users WHERE email = ?', (email))
        login_user(user)
        return url_for('index')
    return render_template('login.html')
        