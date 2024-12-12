from database import get_connection
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email
        self.id = None

    def save(self):
        conn = get_connection()
        conn.execute('INSERT INTO users(email, nome) values(?,?)', (self.email, self.nome))
        conn.commit()
        conn.close()
        return True

    #buscar usuário 
    @classmethod
    def find(cls, **kwargs):
        conn = get_connection()
        if 'email' in kwargs.keys():
            res = conn.execute('SELECT * from users where email = ?', (kwargs['email'],))
        elif 'id' in kwargs.keys():
            res = conn.execute('SELECT * from users where id = ?', (kwargs['id'],))
        else:
            raise AttributeError('A busca deve ser feita por email ou id.')
        data = res.fetchone()
        if data:
            user = User(nome=data['nome'], email=data['email'])
            user.id = data['id']
            return user
        return None
    
    @classmethod
    def all(cls):
        conn = get_connection()
        users = conn.execute('SELECT * FROM users').fetchall()
        return users