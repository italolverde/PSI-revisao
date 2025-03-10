from sqlalchemy.orm import Mapped, mapped_column
from database import Base, session
from flask_login import UserMixin

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
