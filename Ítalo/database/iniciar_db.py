import sqlite3
import os

SQL = 'database.sql'
DATABASE = 'database.db'

dirname = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dirname,SQL)) as f:
    conn = sqlite3.connect(os.path.join(dirname,DATABASE))
    conn.executescript(f.read())
    conn.commit()
    conn.close()