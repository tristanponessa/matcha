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

"""

import sqlite3
import sys
import os
from typing import List, Dict
from matcha_app.profile_db import db_to_file

class Sql_cmds:

    #fetch_opti - 'SELECT json_field FROM users WHERE email='iemail'
    fetch = 'SELECT * FROM {}'
    insert = "INSERT INTO {} ('{}') VALUES ('{}')"
    add_col = 'ALTER TABLE {} ADD {} {}'
    #create_table_opti = "CREATE TABLE users ('email' VARCHAR(100))"
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


def Sexec_sql(sql_cmd : str, *args: List[str]) -> List[Dict[str, str]]:
    with open('./matcha_app/log.txt', 'w+') as f:
        print(f'{sql_cmd} \n', file=f)
    with SQLite() as cur:
        fsql_cmd = sql_cmd.format(*args)
        cur.execute(fsql_cmd)
        res = cur.fetchall()
        return res
        # get output put in log


from matcha_app.profile_db import *
def exec_sql(sql_cmd : str) -> List[Dict[str, str]]:
    with open('./matcha_app/log.txt', 'w+') as f:
        print(f'{sql_cmd} \n', file=f)
    db_to_file('db.txt')
    with SQLite() as cur:
        cur.execute(sql_cmd)
        res = cur.fetchall()
        return res
        # get output put in lo

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



