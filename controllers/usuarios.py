from flask import Blueprint, request, render_template, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required
from database import Base, session #Importando do arquivo INIT da pasta database, por isso não preciso especificar arquivo
from models.usuarios import Usuarios #importando classe Usuarios do arquivo models/usuarios

usuarios_bp = Blueprint(name='usuarios', #Valores explicados no arquivo mvc.md
                        import_name=__name__,
                        template_folder="templates",
                        url_prefix="/usuarios")

@usuarios_bp.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        users = session.query(Usuarios).all()
        for user in users:
            if nome == user.nome: #Checa se o nome do input é igual ao nome de algum usuário ja cadastrado
                return redirect(url_for('usuarios.register')) #Se for, ele redireciona novamente pra pagina de registro
        #Caso não tenha nome repetido:
        novo_user = Usuarios(nome=nome,senha=senha) #Cria um novo objeto da classe Usuarios
        session.add(novo_user) #Adciona ao banco o usuário recém criado
        session.commit() #commit para confirmar a inserção
        login_user(novo_user) #Loga o usuário
        return redirect(url_for('index'))
    else:
        return render_template('usuarios/register.html')

@usuarios_bp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        usuario = session.query(Usuarios).filter(Usuarios.nome == nome).first() #SELECT * FROM usuarios WHERE nome = nome_do_form
        if not usuario: #Caso ele não encontre o usuário, a variavel "usuario" receberá valor "None", dando o valor False pro IF
            print('nome não encontrado')
            return redirect(url_for('usuarios.login')) #Usuário não encontrado, joga o user de volta pra pagina de login
        else:
            if usuario.senha == senha:
                print('Login bem sucedido')
                login_user(usuario) #Comando para logar o usuário na sessão
                usuario = current_user 
            #current_user é uma variavel disponibilizada pelo flask_login para recuperar o usuário logado atualmente pelo comando login_user
                return redirect(url_for('index'))
                
            else:
                print('Senha incorreta')
                return render_template('usuarios/login.html',nome=nome)
    return render_template('usuarios/login.html')

@usuarios_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))