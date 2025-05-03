from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine

engine = create_engine("sqlite:///database/banco.db") #Aqui diz: Modelo do banco (sqlite) e o caminho/nome do arquivo do banco (database/banco.db), é possivel alterar ambos.
session = Session(bind=engine) #Sessão será o responsável por executar as funções dentro do app ativo, assim como faziamos com o "conn = get_connection()"

#CRIAÇÃO DA CLASSE PARA TABELA E FLASK-LOGIN

class Base(DeclarativeBase): #Criação da base das tabelas do sqlalchemy
    pass #está vazia porque ja está herdando tudo que precisa de "DeclarativeBase"
