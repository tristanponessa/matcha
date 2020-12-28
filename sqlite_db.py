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

from check import *



def clean_exit(msg):
    print("exit error : ",msg)
    #close what you need
    sys.exit(0)

def random_account_gen(seed_nb, cur):
    
    data = get_db_tables_from_mysqlmem(cur)
    for table_name, cols in data.items()
        for col in cols:

    print(data)




    """
    sql_cmds = sql_create_tables_cmds()
    d = {}
    for x in sql_cmds:
            
        d[] = 
    data = data.split('`')
    """

    """
    import random
    import string

    random.seed(seed_nb)
    random.choice(choices)
    string.ascii_letters
    string.digits
    print(random.random()) #double
    #for age INTEGER field ran INTEGER between 18-100
    #for name len 5-15 ch/nb
    #sexual  1-3 for 1straight, ....
    """





def exec_sql(cur, sql_cmd):
    #print(sql_cmd)
    cur.execute(sql_cmd)
    res = cur.fetchall()
    return res
    #get output put in log


def db_close(conn, cur):
    if cur:
        cur.close()
    if conn:
        conn.commit()
        conn.close()
    
    #print(f'closing db connection! open? {dbh.open}')
    print(f'closed db connection!')


def dict_factory(cursor, row):
    #get fetch in dict
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def db_conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    return conn, cur

def db_manager():
    """ create a database connection to a SQLite database 
        SQLite database file that does not exist, 
        SQLite automatically creates the new database for you."""

    conn,cur = None,None
    try:
        main()
    except sqlite3.Error as e:
        print(e)
    finally:
        db_close(conn, cur)

class Sql_cmds:

    fetch = 'SELECT * FROM {}'
    insert = 'INSERT {} {} VALUES {}'
    add_col = 'ALTER TABLE {} ADD {} {}'
    create_table = "CREATE TABLE {} ('id' INT PRIMARY KEY)"


def init_db(conn, cur):
    exec_sql(cur, Sql_cmds.create_table.format('users'))
    exec_sql(cur, Sql_cmds.add_col.format('users', 'profile', 'TEXT')) #2gb of text 1,048,576 bytes * 2 > 162 * 2 big msgs


def main():
    conn, cur = db_conn()
    init_db(conn, cur)

import json
def dict_to_str(idict):
    return json.dumps(idict)
def str_to_dict(istr):
    return json.loads(istr)


if __name__ == '__main__':
    db_mananger()



 import rstr
>>> rstr.xeger(r'[A-Z]\d[A-Z] \d[A-Z]\d')
u'M5R 2W4'

class LiteRegex:

    anb = r'[0-9]+'
    alower = r'[a-z]+'
    aupper = r'[A-Z]+'
    asym = r'[_+-*/,;!~%&*]+'
    email = r'^[a-zA-Z0-9_]@[hotmail|outlook|gmail].[com|fr]$'


    import re
    #password
    checks = (anb, alower, aupper, asym)
    if all(re.match(x, istr) for x in checks):
        is password

    literegex_match(istr):


    email = 'x',5, 
        

class Regex:

    email = r'^[a-zA-Z0-9_]+@[hotmail|outlook|gmail].[com|fr]$'
    pwd = []{2}
 