import sqlite3
import os

DATABASE = 'database.db'
dirname = os.path.dirname(os.path.realpath(__file__))

def get_connection():    
    conn = sqlite3.connect(os.path.join(dirname, DATABASE))
    conn.row_factory = sqlite3.Row
    return conn
