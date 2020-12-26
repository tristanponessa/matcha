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

db_name = './matcha.db'

def print_db_tables(cur):
    #x = "SELECT * FROM sqlite_master where type='table'"
    x ="PRAGMA table_info(users)"
    r = execute_sql(cur, x)
    
    for p in r:
        print('----')
        for k,v in p.items():
            print(k, ':', v)


def clean_exit(msg):
    print("exit error : ",msg)
    #close what you need
    sys.exit(0)

def random_account_gen(seed_nb):
    pass
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

def sql_create_tables_cmds():

    users = """CREATE TABLE `users`
       (`id` INTEGER PRIMARY KEY,
        `user_name` TEXT,
        `first_name` TEXT,
        `last_name` TEXT,
        `mail` TEXT,
        `password` TEXT,
        `age` TEXT,
        `intro` TEXT,
        `sexual_orientation` TEXT,
        `tags` TEXT,
        `votes` TEXT,
        `profile_pic` TEXT,
        `pics` TEXT,
        `msgs` TEXT,
        `geolocalisation` TEXT)
        """

    pics = """CREATE TABLE `pics` (
        `id` INTEGER PRIMARY KEY,
        `userid` INTEGER,
        `img` TEXT,
        FOREIGN KEY (userid) REFERENCES users(id)
        )"""

    scores = """CREATE TABLE `scores` (
        `id` INTEGER PRIMARY KEY,
        `from_userid` INTEGER,
        `to_userid` INTEGER,
        FOREIGN KEY (from_userid) REFERENCES users(id)
        FOREIGN KEY (to_userid) REFERENCES users(id)
      )"""

    msgs = """CREATE TABLE `msgs` (
        `id` INTEGER PRIMARY KEY,
        `userid` INTEGER,
        `to_userid` INTEGER,
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
        conn = sqlite3.connect(":memory:")
        #load db with lots of fake accounts if dont exist
        conn.row_factory = dict_factory #fetchall is dict
        cur = conn.cursor()

        x = sql_create_tables_cmds()
        create_tables(cur, x)
        print_db_tables(cur)

    except sqlite3.Error as e:
        print(e)
    finally:
        db_close(conn, cur)
        #os.remove(db_file)
        


if __name__ == '__main__':
    db_init(db_name)


 