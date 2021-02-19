import sqlite3
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



class SqlCmds:

    __ = {
    'sqlite' : {
                    #'fetch' = "SELECT profile FROM users WHERE profile LIKE {}" #'%email={}%' || '%email={}%'
                    'fetch' : 'SELECT profile FROM users WHERE email="{}"',
                    'fetch_all': 'SELECT * FROM users',
                    'insert' : "INSERT INTO users ('{}', '{}') VALUES ('{}', '{}')",
                    'add_col' : 'ALTER TABLE {} ADD {} {}',
                    'create_table' : "CREATE TABLE {} ('id' INTEGER PRIMARY KEY AUTOINCREMENT)",
                    #'delete_row' : "DELETE FROM {} WHERE {}='{}'",
                    'update' : 'UPDATE users SET profile="{}" WHERE email="{}"'
                }
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


def init_db(dbname='sqlite'):
    if dbname == 'sqlite':
        file_paths.if_file_del(file_paths.sqlitefile)
        file_paths.create_file(file_paths.sqlitefile)
        db_exec(SqlCmds.__['sqlite']['create_table'].format('users'))
        db_exec(SqlCmds.__['sqlite']['add_col'].format('users', 'email', 'TEXT'))
        db_exec(SqlCmds.__['sqlite']['add_col'].format('users', 'profile', 'TEXT'))

"""
def setup_db(dbfile, action):
    
    #if_file_del('./matcha.db')
    if action == 'new':
        randstr = gen_rand_nosymbs(5) 
        sqlitefile =  
        if not os.path.exists(file_paths.sqlitefile):
            init_db()
    profiles = create_profiles(0)
    load_profiles_in_db(profiles)
"""

#BIG FN

"""
def spy_on(on):
    def inner(*args, **kwargs):
        db_exec(*args, **kwargs)
        if on:
            db_to_file(file_paths.sqlitefile)
    return inner
"""

def db_exec(cmd) -> 'lst[dct]':
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



    print_log('sqlite', cmd)
    with SQLite() as cur:
        cur.execute(cmd)
        res = cur.fetchall()
        #if len(res) == 1 and isinstance(res[0], dict) and None in res[0].values():
        #    res = []
        return res




def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#########################

#{'birthdate':'03/05/95', 'first_name':'natsirt'}
def get_profiles(data):
    if data == '*':
        ps = db_exec(SqlCmds.__['sqlite']['fetch_all'])
        return [json.loads(p) for p in ps]
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















