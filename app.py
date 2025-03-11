from flask import Flask, request, render_template, url_for, redirect
from flask_login import LoginManager, current_user
from models.usuarios import Usuarios #Importando a CLASSE USUARIOS do arquivo models/user.py
from database import Base, engine, session #Importando Base e Engine do arquivo init da pasta database, por isso não especifico arquivo

from controllers.usuarios import usuarios_bp #Pegando a blueprint das rotas de usuários do arquivo controllers/usuarios
from controllers.livros import livros_bp
from controllers.emprestimos import emprestimos_bp

from models.emprestimos import Emprestimos

app = Flask(__name__)

app.config['SECRET_KEY'] = 'asdfghjkl'

login_manager = LoginManager() #Pega o gerenciador da biblioteca do flask_login

@login_manager.user_loader #Carregador padrão do flask_login, isso é obrigatório
def load_user(user_id):
    return Usuarios.find(id=user_id) #Pega o usuario baseado no ID, por meio dos kwargs (explicado na linha 32 e 33)
    #Esse função find está sendo definida la na linha 31, caso mude o nome la, tem que mudar aqui também

login_manager.init_app(app) #inicia o flask_login dentro do app, faz rodar, bota pra funcionar

with app.app_context():
    Base.metadata.create_all(bind=engine) #Comando para criar as tabelas do banco

app.register_blueprint(usuarios_bp)
app.register_blueprint(livros_bp)
app.register_blueprint(emprestimos_bp)

@app.route('/')
def index():

    emprestimos = session.query(Emprestimos).all() #SELECT * FROM emprestimos || para exibir no index

    #current_user é uma variavel disponibilizada pelo flask_login para pegar o usuário atual estando logado ou não
    if current_user.is_authenticated: #current_user.is_authenticated: Verifica se você está logado e retorna True caso esteja.
        return render_template('index.html', nome=current_user.nome, emprestimos = emprestimos)
    else: #Caso seja um usuário anônimo, ainda não logado pelo comando login_user():
        return render_template('index.html', emprestimos = emprestimos)
    

