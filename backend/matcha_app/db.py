"""


CREATE TABLE if not exists themes (
         id INT NOT NULL PRIMARY KEY,
  		 name varchar(100) not NULL        
        )
        
CREATE TABLE themes (
    themeID int NOT NULL,
    demo_id int,
    PRIMARY KEY (themeID),
    FOREIGN KEY (demo_id) REFERENCES demo(demo_id)); 

ALTER TABLE themes
ADD name VARCHAR(50); 


"""

import sqlite3
import psycopg2 as postgresql_mod

import sys
#sys.path.append('/home/user/Documents/coding/matcha')
#sys.path.append('/home/user/Documents/coding/matcha/matcha_app')
#sys.path.append('/home/user/Documents/coding/matcha/matcha_app/db_files')

import os
from typing import List, Dict
import random
import string
import json
import inspect

from matcha_app.fields import *
from matcha_app import file_paths



MAIN_DB = 'sqlite'

class SqlCmds:
    """
        extendable for other dbs
    """

    sqlite = {
                    #'fetch' = "SELECT profile FROM users WHERE profile LIKE {}" #'%email={}%' || '%email={}%'
                    'fetch' : 'SELECT profile FROM users WHERE email="{}"',
                    'fetch_all': 'SELECT * FROM users',
                    'insert' : "INSERT INTO users ('{}', '{}') VALUES ('{}', '{}')",
                    'add_col' : 'ALTER TABLE {} ADD {} {}',
                    'create_table' : "CREATE TABLE {} ('id' INTEGER PRIMARY KEY AUTOINCREMENT)",
                    #'delete_row' : "DELETE FROM {} WHERE {}='{}'",
                    'update' : 'UPDATE users SET profile="{}" WHERE email="{}"',
                    'foreign_key' : lambda ptr_name,dst_table,dst_field: f"FOREIGN KEY ('{ptr_name}') REFERENCES '{dst_table}'('{dst_field}')"

             }

    postgresql = sqlite #shallow copy, ref to sqlite
    
    fake_db = {
                    #'fetch' = "SELECT profile FROM users WHERE profile LIKE {}" #'%email={}%' || '%email={}%'
                    'fetch' : "",
                    'fetch_all': "",
                    'insert' : "",
                    'add_col' : "",
                    'create_table' : "",
                    #'delete_row' : "DELETE FROM {} WHERE {}='{}'",
                    'update' : ""
             }
    

    


class SQLite:
    """
        auto creates file if dont exist
        there must be a connexion for every thread, use cont.manag.
    """
    def __init__(self, file=file_paths.sqlitefile):
        self.file = file
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = self.dict_factory
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, type, value, traceback):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.commit()
            self.conn.close()
        #print(f'closed instance db connection!')
    
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

class Postgresql:
    """
        auto creates file if dont exist
        there must be a connexion for every thread, use cont.manag.
    """
    def __init__(self, file=None):
        self.file = file
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = postgresql_mod.connect(host="localhost", 
                                            user="trponess", 
                                            password="0000", 
                                            dbname="main_db", 
                                            charset='utf8mb4',
                                            host='',
                                            port='',
                                            cursor_factory=postgresql_mod.extras.RealDictCursor) 
        #print(f'db connection : open ? {self.conn.open}') 
        #self.conn.row_factory = self.dict_factory
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, type, value, traceback):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.commit()
            self.conn.close()
        #print(f'closed instance db connection!')
    

class FakeDb:
    pass


def init_db(dbname):
    if dbname == 'sqlite':
        file_paths.if_file_del(file_paths.sqlitefile)
        file_paths.create_file(file_paths.sqlitefile)
    if dbname == 'postgresql':
        #check exsitance of db, check connect...
        pass
    if dbname == 'fakedb':
        #file_paths.if_file_del(file_paths.fakedbfile)
        #file_paths.create_file(file_paths.fakedbfile)
        pass

    db_exec(dbname, 'create_table', ['users'])
    db_exec(dbname, 'add_col', ['users', 'email', 'TEXT'])
    db_exec(dbname, 'add_col', ['users', 'profile', 'TEXT'])


def db_exec(db, action, args):
    """
        -writes in log
        -converts json to str for db ; reverse for return
        -call a new cursor each time for processsss
        -returns
        from : dct_factory() in class SQLite()
        RES []
        RES [{'profile': }] SELECT profile FROM users WHERE email="email"
        RES [{'id' : 8 , 'email' : '@' , 'profile': "{'birthdate': '', }" OR None, ...]
    """

    cmd = SqlCmds.__dict__[db][action].format(*args)

    if db == 'fakedb':
        pass
    if db == 'sqlite':
        
        with SQLite() as cur:
            cur.execute(cmd)
            res = cur.fetchall()
            return res
    
    if db == 'postgresql':
        with Postgresql() as cur:
            cur.execute(cmd)
            res = cur.fetchall()
            return res

    




#########################

#{'birthdate':'03/05/95', 'first_name':'natsirt'}
def get_profiles(data):
    if data == '*':
        ps = db_exec(SqlCmds.__['sqlite']['fetch_all'])
        return [json.loads(p['profile']) for p in ps]
    elif 'email' in data.keys():
        p = db_exec(SqlCmds.__['sqlite']['fetch'].format(data['email']))
        return json.loads(p[0]['profile']) if len(p) == 1 else None
    else:
        all_profiles = db_exec(SqlCmds.__['sqlite']['fetch_all'])

        return [json.loads(p['profile']) for p in all_profiles if is_subdct(data, json.loads(p['profile']))] 

def stock_profiles(ps):
    for p in ps:
        if not get_profiles({'email': p['email']}):
            db_exec(SqlCmds.__['sqlite']['insert'].format('email', 'profile', p['email'], json.dumps(p)))
        else:
            db_exec(SqlCmds.__['sqlite']['update'].format(json.dumps(p), p['email']))

def load_db(dbname, what):
    if dbname == 'sqlite':
        ps = []
        if what == 'random':
            ps = create_profiles(0)
        if what == 'fake':
            ps = json.load(open(file_paths.fakedb, 'r'))
        stock_profiles(ps)



# DISPLAY FUNS
def print_profile(profile, file=None):
    top = bottom = '-' * 50
    print(top, file=file)
    n = 0
    for k, v in profile.items():
        print(f'{n}<{k}>'.center(30, '*'), file=file)
        if isinstance(v, list):
            for i, e in enumerate(v):
                print(f'    {i} > {e}', file=file)
        elif isinstance(v, dict):
            for a, b in v.items():
                print(f'    {a} > {b}', file=file)
        else:
            print(f'    {v}', file=file)
        n += 1
    print(bottom, file=file)

#can cause recurisitvy prolem if called inside db_exec, use decorator
def db_to_file(file):
    with open(file, 'w+') as f:
        for pro in get_profiles('*'):
            print_profile(pro, f)

def print_log(dbname, cmd):
    with open(file_paths.generallog, 'a+') as f:
        print(f'{Timestamp.get_now_time()} {dbname} >> {cmd} \n', file=f)















