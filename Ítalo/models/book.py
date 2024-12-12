from database import get_connection

class Book:
    def __init__(self, titulo, user_id):
        self.titulo = titulo
        self.user_id = user_id

    def save(self):
        conn = get_connection()
        conn.execute('INSERT INTO books(titulo, user_id) values(?,?)', (self.titulo, self.user_id))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def all(cls):
        conn = get_connection()
        books = conn.execute('SELECT * FROM books').fetchall()
        return books