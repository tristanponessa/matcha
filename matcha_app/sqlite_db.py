"""
Never use Python string operations to dynamically create a SQL statement string. Using Python string operations to assemble a SQL statement string leaves you vulnerable to SQL injection attacks. SQL injection attacks 

    have to manually connect to root localhost and create another user to whom you will connect here
    default engine is innoDB
    tous les emojis et autres sont sur 4 octets
    UTF8 de MySQL ne peut coder les caracteres que sur 3 octets
    depuis ver5 MySQL permet le codage sur 4 octets mais le codage doit être modifié en UTF8mb4

    show tables;
    SHOW TABLE STATUS;
    describe users;

    normally the project should be done with an orm for better db manag, the project demands us to use an ancient technik which is brut sql calls in python, 
    the proeject might not be completed at the best

    geo location in db shouldnt be there but the pro demande to always locate despite an eventual block, ill store the last place just in case
    tmp vars like sign up token , received msg alert, recent like , is stored in session object

    class SQLite():
    def __init__(self, file='sqlite.db'):
        self.file=file
    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()
"""

import sqlite3
import sys
import os


class Sql_cmds:

    fetch = 'SELECT * FROM {}'
    insert = "INSERT INTO {} ('{}') VALUES ('{}')"
    add_col = 'ALTER TABLE {} ADD {} {}'
    create_table = "CREATE TABLE {} ('id' INTEGER PRIMARY KEY AUTOINCREMENT)"
    delete_row = "DELETE FROM {} WHERE {}='{}'"


class SQLite:
    """there must be a connexion for every thread, use cont.manag."""
    def __init__(self, file='matcha.db'):
        self.file = file
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = dict_factory
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, type, value, traceback):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.commit()
            self.conn.close()
        #print(f'closed instance db connection!')


def init_db():
    exec_sql(Sql_cmds.create_table.format('users'))
    exec_sql(Sql_cmds.add_col.format('users', 'profile', 'TEXT')) #2gb of text 1,048,576 bytes * 2 > 162 * 2 big msgs


def exec_sql(sql_cmd):
    print(sql_cmd)
    with SQLite() as cur:
        cur.execute(sql_cmd)
        res = cur.fetchall()
        return res
        # get output put in log


def dict_factory(cursor, row):
    # get fetch in dict
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


"""
def db_conn():
    conn = sqlite3.connect("matcha.db")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    return cur

def db_close(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.commit()
        conn.close()

def clean_exit(msg):
    print("exit error : ",msg)
    # close what you need
    sys.exit(0)

"""

"""
if __name__ == '__main__':
    cur = db_conn()
    init_db(cur)
    r = exec_sql(cur, Sql_cmds.fetch.format('users'))  # 2gb of text 1,048,576 bytes * 2 > 162 * 2 big msgs
    print(r)
    os.remove('matcha.db')
"""



