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

#db_name = './matcha.db'

def get_db_tables_from_mysqlmem(cur):
    t = "SELECT * FROM sqlite_master where type='table'"
    r = execute_sql(cur, t)
    t = [ir['name'] for ir in r]
    print('tables : ', t)

    d = {}
    table_content = {table_name:f'PRAGMA table_info({table_name})' for table_name in t}
    for table_name,table_elem in table_content.items():
        r = execute_sql(cur, table_elem)
        cols = [{'name':ir['name'], 'type': ir['type']} for ir in r]
        d[table_name] = cols
    
    """
    for k,v in d.items():
        print('----')
        print('table: ', k)
        for iv in v:
            print('col: ', iv)
        print()
    
    print(d)
    print(r)
    """
    return d

def print_db_data(cur):
    pass
    """
    for p in r:
        print('----')
        for k,v in p.items():
            print(k, ':', v)
    """


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


class db_elem:

    def __init__(self, **data):
        """
        table_name 
        itype  
        err_msg  
        irange  
        col_name 
        ref   #if foreign
        """

        self.__dict__ = data.clone()
    
    def insert_self():
        """put values in db"""
    
    def check_valid():
    
    def random_fill_Self():

{'table_name':'users', 'table_name':'users'}
db_elem()




def sql_create_tables_cmds():
    """autoincrement, constraint added auto"""
    """I USED BIGINT TO REFERENCE A FOREIGN KEY THANKS SQLITE"""

    limits = {}
    limits['age'] = [range(18,100)]
    ['name'] = [len()]

    def check_data_format(name, val):
    """web form user insert data check"""
        if name == 'age':
            error_msg = "not a valid age"
            f = [str(n) for n in range(18-100)]
            if val not in f:
                return error_smg
            #else none



    tables = {}

    tables['users'] = {}
    ['FOREIGN'] = ['votes', 'mgs', 'tags', 'pics']
    ['PRIMARY KEY'] = ['id']
    ['INTEGER'] = ['age', '']
    ['TEXT'] = ['first_name', 'last_name', 'password', 'intro', 'mail', 'sexual_orientation', ''
        'user_name', 
        'first_name', 
        'last_name', 
        'mail', 
        'password',
        'profile_pic', 
        'pics'
        ]
    cols = [
        'id',
        'user_name', 
        'first_name', 
        'last_name', 
        'mail', 
        'password', 
        'age', 
        'intro', 
        'sexual_orientation', 
        'tags', 
        'votes', 
        'profile_pic', 
        'pics', 
        'msgs', 
        'geolocalisation']
    types = ['INTEGER PRIMARY KEY', 'TEXT', 'INTEGER','BIGINT']
    for col_name in cols:


    users = """CREATE TABLE `users`
       (`id` INTEGER PRIMARY KEY,
        `user_name` TEXT,
        `first_name` TEXT,
        `last_name` TEXT,
        `mail` TEXT,
        `password` TEXT,
        `age` INTEGER,
        `intro` TEXT,
        `sexual_orientation` TEXT,
        `tags` TEXT,
        `votes` INTEGER,
        `profile_pic` TEXT,
        `pics` TEXT,
        `msgs` TEXT,
        `geolocalisation` TEXT)
        """
    


    pics = """CREATE TABLE `pics` (
        `id` INTEGER PRIMARY KEY,
        `userid` BIGINT,
        `img` TEXT,
        FOREIGN KEY (userid) REFERENCES users(id)
        )"""

    scores = """CREATE TABLE `scores` (
        `id` INTEGER PRIMARY KEY,
        `from_userid` BIGINT,
        `to_userid` BIGINT,
        FOREIGN KEY (from_userid) REFERENCES users(id)
        FOREIGN KEY (to_userid) REFERENCES users(id)
      )"""

    msgs = """CREATE TABLE `msgs` (
        `id` INTEGER PRIMARY KEY,
        `userid` BIGINT,
        `to_userid` BIGINT,
        `msg` TEXT,
        FOREIGN KEY (userid) REFERENCES users(id)
        FOREIGN KEY (to_userid) REFERENCES users(id)
      )"""

    return [users, pics, scores, msgs]

def create_tables(cur, sql_cmds):
    for x in sql_cmds:
        execute_sql(cur, x)

def execute_sql(cur, sql_cmd):
    #print(sql_cmd)
    cur.execute(sql_cmd)
    res = cur.fetchall()
    return res
    #return searches
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


"""
def error_msgs(iid):
    d = {'conn_error':'failed to connect'}
    return d[iid]
"""

def db_init(db_file):
    """ create a database connection to a SQLite database 
        SQLite database file that does not exist, 
        SQLite automatically creates the new database for you."""

    conn,cur = None,None
    try:
        #":memory:"
        #conn = sqlite3.connect(db_file)
        conn = sqlite3.connect(":memory:") #generates one time session no file
        #load db with lots of fake accounts if dont exist
        conn.row_factory = dict_factory #fetchall is dict
        cur = conn.cursor()

        x = sql_create_tables_cmds()
        create_tables(cur, x)
        #get_db_tables_from_mysqlmem(cur)
        #print_db_tables(cur)
        random_account_gen(14, cur)

    except sqlite3.Error as e:
        print(e)
    finally:
        db_close(conn, cur)
        #os.remove(db_file)
        


if __name__ == '__main__':
    db_init(None)


 