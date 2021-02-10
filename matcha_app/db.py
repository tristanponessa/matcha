import sqlite3
import sys
sys.path.append('/home/user/Documents/coding/matcha')
sys.path.append('/home/user/Documents/coding/matcha/matcha_app')
sys.path.append('/home/user/Documents/coding/matcha/matcha_app/db_files')

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
                    'fetch_profile' : 'SELECT profile FROM users WHERE email="{}"',
                    'fetch_all': 'SELECT profile FROM users',
                    'insert' : "INSERT INTO users ('{}') VALUES ('{}')",
                    'add_col' : 'ALTER TABLE {} ADD {} {}',
                    'create_table' : "CREATE TABLE {} ('id' INTEGER PRIMARY KEY AUTOINCREMENT)",
                    'delete_row' : "DELETE FROM {} WHERE {}='{}'",
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
        db_exec('create_table', {'table': 'users'}, dbname)
        db_exec('create_table', {'table': 'users', 'field': 'email', 'type': 'TEXT'}, dbname)
        db_exec('create_table', {'table': 'users', 'field': 'profile', 'type': 'TEXT'}, dbname)

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

def spy_on(func):
    def inner(*args, **kwargs):
        #func(*args, **kwargs)
        #db_to_file(file_paths.sqlitefile)
        return func(*args, **kwargs)
    return inner

@spy_on
def db_exec(action, data:'{email:dct}', out=False, dbname='sqlite') -> Dict[str, str]:
    """
        -writes in log
        -converts json to str for db ; reverse for return
    """
    if 'profile' in data:
        data['profile'] = json.dumps(data['profile']) #dct to str

    cmd = SqlCmds.__[dbname][action].format(*data.values())

    if dbname == 'sqlite':

        if out:
            pass
            # with open(file_paths.generallog, 'w+') as f:
            #    print(f'{dbname} >> {cmd} \n', file=f)


        with SQLite() as cur:
            cur.execute(cmd)
            res = cur.fetchall()
            res = [json.loads(r['profile']) for r in res] #convert str to dct
            return res





def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#########################

#{'birthdate':'03/05/95', 'first_name':'natsirt'}
def get_profiles(data):
    all_profiles = db_exec('fetch_all', {}, 'sqlite')
    return (p for p in all_profiles if data <= p)

def profile_exists(email):
    return len(db_exec('fetch_profile', {'email': email}, 'sqlite')) == 1

def stock_profiles(ps):
    for p in ps:
        if len(db_exec('fetch_profile', {'email': p['email']}, 'sqlite')) == 0:
            db_exec('insert', {'email': p['email']}, 'sqlite')
            db_exec('insert', {'profile': p}, 'sqlite')
        else:
            db_exec('update', {'profile': p}, 'sqlite')


def create_profiles(master_seed):

    nb_users = 10
    min_seed = 0#(nb_users * master_seed)
    max_seed = 99999#min_seed + nb_users

    profiles = []  # to put into db list of dicts
    seed_nbs = tuple(random.randint(0,9999) for _ in range(nb_users))
    emails = tuple(Email.random_(seednb) for seednb in seed_nbs)
    field_fns = get_field_fns('random_')

    for seed_nb, email in zip(seed_nbs, emails):
        profile = {'email' : email}
        for clsname, randfn in field_fns.items():
            if clsname != 'Email':
                if randfn.__code__.co_argcount == 2:
                    profile[clsname.lower()] = randfn(emails, seed_nb)
                else:
                    profile[clsname.lower()] = randfn(seed_nb)
        profiles.append(profile)
    return profiles


def load_db(dbname, what):
    if dbname == 'sqlite':
        ps = []
        if what == 'random':
            ps = create_profiles(0)
        if what == 'fake':
            ps = json.load(file_paths.fakedb)

            for p in ps:
                db_exec('insert', {'email': p['email']}, 'sqlite')
                db_exec('insert', {'profile': p}, 'sqlite')


# DISPLAY FUNS
def print_profile(profile, file=None):
    top = bottom = '-' * 50
    print(top, file=file)
    for k, v in profile.items():
        print(f'<{k}>'.center(15, '*'), file=file)
        if isinstance(v, list):
            for i, e in enumerate(v):
                print(f'    {i} > {e}', file=file)
        elif isinstance(v, dict):
            for a, b in v.items():
                print(f'    {a} > {b}', file=file)
        else:
            print(f'    {v}', file=file)
    print(bottom, file=file)





def db_to_file(file):
    with open(file, 'w+') as f:
        for pro in db_exec('fetch_all', {}, 'sqlite'):
            print_profile(pro, f)

















