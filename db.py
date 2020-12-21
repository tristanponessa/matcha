"""
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

import sys

import pymysql

def clean_exit(msg):
    print("exit error : ",msg)
    #close what you need
    sys.exit(0)

def sql_create_tables_cmds():

    users = """CREATE TABLE if not exists `users`
       (`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `user_name` VARCHAR(50) NOT NULL,
        `first_name` VARCHAR(50) NOT NULL,
        `last_name` VARCHAR(50) NOT NULL,
        `mail` VARCHAR(100) NOT NULL,
        `password` VARCHAR(255) NOT NULL,
        `age` VARCHAR(255) NOT NULL,
        `intro` VARCHAR(255) NOT NULL,
        `sexual_orientation` VARCHAR(255) NOT NULL,
        `tags` VARCHAR(255) NOT NULL,
        `votes` VARCHAR(255) NOT NULL,
        `profile_pic` VARCHAR(255) NOT NULL,
        `pics` VARCHAR(255) NOT NULL,
        `msgs` VARCHAR(255) NOT NULL,
        `geolocalisation` VARCHAR(255) NOT NULL, 1
        """

    pics = """CREATE TABLE if not exists `pics` (
        `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `userid` INT(11) NOT NULL,
        `img` VARCHAR(200) NOT NULL,
        FOREIGN KEY (userid) REFERENCES users(id)
        )"""

    scores = """CREATE TABLE if not exists `scores` (
        `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `from_userid` INT(11) NOT NULL,
        `to_userid` INT(11) NOT NULL,
        FOREIGN KEY (from_userid) REFERENCES users(id)
        FOREIGN KEY (to_userid) REFERENCES users(id)
      )"""

    msgs = """CREATE TABLE if not exists `msgs` (
        `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `userid` INT(11) NOT NULL,
        `to_userid` INT(11) NOT NULL,
        `msg` TEXT NOT NULL,
        FOREIGN KEY (userid) REFERENCES users(id)
        FOREIGN KEY (to_userid) REFERENCES users(id)
      )"""

    return [users, pics, scores, msgs]

def create_tables(cur, sql_cmds):
    for x in sql_cmds:
        execute_sql(cur, x)

def execute_sql(cur, sql_cmd):
    print(sql_cmd)
    cur.execute(sql_cmd)
    #res = cur.fetchall()
    return res
    #return searches
    #get output put in log

def mysql_connection():
    #uses TCP/IP socket , better in case i work on mac or windows ; port 3306 by default 
    dbh = pymysql.connect(host="localhost", 
                            user="trponess", 
                            password="0000", 
                            db="main_db", 
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor) 
    print(f'db connection : open ? {dbh.open}') 
    return dbh

def mysql_close(dbh):
    print(f'closing db connection! open? {dbh.open}')
    dbh.close()
    #better check
    print(f'closed db connection! open? {dbh.open}')

"""
def error_msgs(iid):
    d = {'conn_error':'failed to connect'}
    return d[iid]
"""

def main():

    try:
        dbh = mysql_connection()
        with dbh.cursor() as cur:
            sql_cmds = sql_create_tables_cmds()
            create_tables(cur, sql_cmds)

    except Exception as e: 
        print(f"EXCEPTION error > {e}") 
    finally:
        #context manager auto closes cursor whatever happens
        mysql_close(dbh)




####################################################################  
main()


def 