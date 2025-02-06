## <span style="color: #ff5c5c;">! NESTE DOCUMENTO ESTOU SUPONDO QUE O ALUNO JA SABE O BÁSICO DO FLASK, AQUI SERÁ EXPLICADO APENAS AS COISAS RELACIONADAS DIRETAMENTE A BIBLIOTECA "FLASK-LOGIN" !</span>  
## <span style="color: #ff5c5c;">! NÃO ESTAREI ABORDANDO SQLALCHEMY POR NÃO SER O FOCO DO MATERIAL !</span>  

## <span style="color: #007bff;"> Caso queira testar o site exemplo que fiz, crie e ative uma env e baixe as bibliotecas do arquivo requirements.txt </span>  

## <span style="color: #007bff;"> pip install -r requirements.txt </span>  

--

# Criação da classe usuário

## Herança da classe Usuarios: **Base** e **UserMixin**
---
- A Classe **Base** é apenas uma cópia da classe **"DeclarativeBase"**, que é dada pelo **sqlalchemy**
- A Classe **UserMixin** serve para transformar aquela classe em um usuário logável pelo **flask-login**

## Criação: 
```py
class Usuarios(Base, UserMixin): #Herda Base (sqlalchemy) e UserMixin (Flask-Login) para servir de usuário ao mesmo tempo que é armazenado no banco
    __tablename__ = 'usuarios' #Usuários serão armazenados na tabela "usuarios" do banco
    id:Mapped[int] = mapped_column(primary_key=True)
    nome:Mapped[str]
    senha:Mapped[str]

    @classmethod #Método de classe, apenas uma função, mas que roda pela classe ( Ex: Usuarios.find() )
    def find(cls, **kwargs): #cls é o mesmo de "self" para POO, porém, para classe, pois aqui não estamos especificando um objeto, mas sim toda a classe.
        #Kwargs quer dizer que iremos receber um valor nomeado, por exemplo Usuarios.find(id=1), isso quer dizer que receberemos um dicionario {id: 1}
        #Assim, podemos verificar o que estamos tentando pegar apenas checando se exite esse argumento no dicionario:
        if 'id' in kwargs: #Checa se existe a chave id
            return session.query(cls).filter_by(id=kwargs['id']).first() # SELECT * FROM usuarios WHERE id = id;
        else: 
            raise AttributeError('A busca deve ser feita por id.')
```
## Os principais pontos são:
- Os atributos da classe, que serão passadas também para o usuário
- Classe find, que servirá para carregar o usuário a partir da classe
---
# Configuração do Flask-Login
### Criação do Login Manager:
```py
from flask_login import LoginManager
login_manager = LoginManager() #Servirá para as configurações abaixo
```
### Configuração do User Loader
```py
@login_manager.user_loader #Carregador de usuário para o flask-login
def load_user(user_id):
    return Usuarios.find(id=user_id) #Pega o usuario pelo ID, função criada na classe Usuarios
```
### Inicialização do Flask-Login no app
```py
login_manager.init_app(app)
```

### Também será necessário configurar uma SECRET_KEY para a criação de novos usuários
```py
app.config['SECRET_KEY'] = 'chave_secreta'
```
# Comandos:
### Após essa breve configuração do flask-login ele ja está pronto para uso, aqui estão os comandos básicos de manipulação do usuário:
<span style="color: #ff5c5c;">! LEMBRANDO QUE OS COMANDOS LISTADOS AQUI ABAIXO PRECISAM SER IMPORTADOS DA BIBLIOTECA flask_login !</span>  
```py
login_user(usuario) #--> Recebe um objeto da classe Usuarios e o torna o usuário atual da sessão

logout_user() #--> Remove o Usuário atual da sessão

current_user #--> Variável disponibilizada pela biblioteca, ela é o usuário atual da sessão

@login_required #--> Vem entre a definição da rota e a função da rota, serve para bloquear uma rota, tornando-a acessível apenas para usuários logados

is_authenticated #--> Propriedade do current_user, retorna True caso tenha um usuário logado

is_anonymous #--> O mesmo do is_authenticated, porém, com o resultado invertido, retorna True caso NÃO TENHA um usuário logado
```