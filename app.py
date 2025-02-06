from flask import Flask, request, render_template, url_for, redirect
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, Session
from sqlalchemy import create_engine, String, ForeignKey
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = 'asdfghjkl'

engine = create_engine("sqlite:///banco.db") #Aqui diz: Modelo do banco (sqlite) e o nome do arquivo do banco (banco.db), é possivel alterar ambos.
session = Session(bind=engine) #Sessão será o responsável por executar as funções dentro do app ativo, assim como faziamos com o "conn = get_connection()"

login_manager = LoginManager() #Pega o gerenciador da biblioteca do flask_login

@login_manager.user_loader #Carregador padrão do flask_login, isso é obrigatório
def load_user(user_id):
    return Usuarios.find(id=user_id) #Pega o usuario baseado no ID, por meio dos kwargs (explicado na linha 32 e 33)
    #Esse função find está sendo definida la na linha 31, caso mude o nome la, tem que mudar aqui também

login_manager.init_app(app) #inicia o flask_login dentro do app, faz rodar, bota pra funcionar

#CRIAÇÃO DA CLASSE PARA TABELA E FLASK-LOGIN

class Base(DeclarativeBase): #Criação da base das tabelas do sqlalchemy
    pass #está vazia porque ja está herdando tudo que precisa de "DeclarativeBase"

class Usuarios(Base, UserMixin): #Herda Base (sqlalchemy) e UserMixin (Flask-Login) para servir de usuário ao mesmo tempo que é armazenado no banco
    __tablename__ = 'usuarios' #Usuários serão armazenados na tabela "usuarios" do banco
    id:Mapped[int] = mapped_column(primary_key=True)
    nome:Mapped[str]
    senha:Mapped[str]

    @classmethod #Método de classe, apenas uma função, mas que roda pela classe ( Ex: Usuarios.find() )
    def find(cls, **kwargs): #cls é o mesmo de "self" para POO, porém, para classe, pois aqui não estamos especificando um objeto, mas sim toda a classe.
        #Kwargs quer dizer que iremos receber um valor nomeado, por exemplo Usuarios.find(id=1), isso quer dizer que receberemos um dicionario {id: 1}
        #Assim, podemos verificar o que estamos tentando pegar apenas checando se exite esse argumento no dicionario:
        if 'nome' in kwargs: #Checa se exite a chave nome
            return session.query(cls).filter_by(nome=kwargs['nome']).first() # SELECT * FROM usuarios WHERE nome = nome;
        elif 'id' in kwargs: #Checa se existe a chave id
            return session.query(cls).filter_by(id=kwargs['id']).first() # SELECT * FROM usuarios WHERE id = id;
        else: 
            raise AttributeError('A busca deve ser feita por nome ou id.') #Apenas um return de erro caso não tenha nenhum dos argumentos.

with app.app_context():
    Base.metadata.create_all(bind=engine) #Comando para criar as tabelas do banco

@app.route('/')
def index():
    user = current_user
    #current_user é uma variavel disponibilizada pelo flask_login para recuperar o usuário logado atualmente pelo comando login_user
    try:
        return render_template('index.html', nome=user.nome)
    except:
        return render_template('index.html')
@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        users = session.query(Usuarios).all()
        for user in users:
            if nome == user.nome: #Checa se o nome do input é igual ao nome de algum usuário ja cadastrado
                return redirect(url_for('register')) #Se for, ele redireciona novamente pra pagina de registro
        #Caso não tenha nome repetido:
        novo_user = Usuarios(nome=nome,senha=senha) #Cria um novo objeto da classe Usuarios
        session.add(novo_user) #Adciona ao banco o usuário recém criado
        session.commit() #commit para confirmar a inserção
        login_user(novo_user) #Loga o usuário
        return redirect(url_for('index'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        usuario = session.query(Usuarios).filter(Usuarios.nome == nome).first() #SELECT * FROM usuarios WHERE nome = nome_do_form
        if not usuario: #Caso ele não encontre o usuário, a variavel "usuario" receberá valor "None", dando o valor False pro IF
            print('nome não encontrado')
            return redirect(url_for('login')) #Usuário não encontrado, joga o user de volta pra pagina de login
        else:
            if usuario.senha == senha:
                print('Login bem sucedido')
                login_user(usuario) #Comando para logar o usuário na sessão
                usuario = current_user 
            #current_user é uma variavel disponibilizada pelo flask_login para recuperar o usuário logado atualmente pelo comando login_user
                return redirect(url_for('index'))
                
            else:
                print('Senha incorreta')
                return render_template('login.html',nome=nome)
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))