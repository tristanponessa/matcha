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

import random
import string
from typing import List
from matcha_app.gen_random import *
from matcha_app.dict_ops import *
from matcha_app.zemail import *
from matcha_app.security_ import *




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


###########################################################################################

# db + dict_ops

# DB ACTION
def load_profiles_in_db(profiles: List[Dict[str, str]]) -> None:
    for profile_dict in profiles:
        profile_str = dict_to_str(profile_dict)
        exec_sql(Sql_cmds.insert.format('users', 'profile', profile_str))


def update_profile(email, data):
    profile = fetch_profiles({'email': email})[0]
    unik_id = fetch_unikid_profile_by_email(email)
    exec_sql(Sql_cmds.delete_row.format('users', 'id', unik_id))
    profile.update(data)
    load_profiles_in_db([profile])  # will have new unik id


def del_profile(email):
    profile = fetch_profiles({'email': email})[0]
    unik_id = fetch_unikid_profile_by_email(email)
    exec_sql(Sql_cmds.delete_row.format('users', 'id', unik_id))


# CHECK FUNS
def profile_get(email, key):
    return fetch_profiles({'email': email})[0][key]


def profile_exists(email, fetch=False):
    x = fetch_profiles({'email': email})
    if fetch:
        return x
    return len(x) == 1
    # return len(fetch_profiles({'email': email})) == 1


def is_profile_signedIn(email):
    return fetch_profiles({'email': email})[0]['signed_in']


# GET FUNS
def get_general_profile_data(email):
    profile = fetch_profiles({'email': email})[0]
    del profile['blocked']
    del profile['activated']
    del profile['signed_in']
    del profile['msgs']
    return profile


def fetch_unikid_profile_by_email(email):
    users_table = exec_sql(Sql_cmds.fetch.format('users'))
    for row_nb in range(len(users_table)):
        unik_id = users_table[row_nb]['id']
        profile_str = users_table[row_nb]['profile']
        if email in profile_str:
            return unik_id


def fetch_all_emails():
    profiles_dct_lst = extract_profiles_from_db()
    emails = []
    for profile_dct in profiles_dct_lst:
        emails.append(profile_dct['email'])
    return emails


# MODIFY FUNS
# def block_user(email):
#    update_profile(email, {'blocked':True})

def like_user(from_email, to_email):
    profile = fetch_profiles({'email': from_email})[0]
    # likes = dict_val_similar_key(profile, 'like')
    likes = profile['likes'].append(to_email)
    update_profile(from_email, {'likes': likes})


def format_profile(profile):
    # fields not seen on sign page
    profile['blocked'] = False
    profile['activated'] = False
    profile['signed_in'] = False
    profile['likes'] = []
    profile['msgs'] = []
    return profile


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


def db_to_file(dbfile=None):
    with open(dbfile, 'w+') as f:
        for pros in extract_profiles_from_db():
            print_profile(pros, f)


###############TOP CRUCIAL METHODS##############################

def extract_profiles_from_db() -> List[dict]:
    users_table = exec_sql(Sql_cmds.fetch.format('users'))
    col_str = 'profile'
    profiles_dct_lst = []
    for row_nb in range(len(users_table)):
        profile_str = users_table[row_nb][col_str]
        profile_dct = str_to_dict(profile_str)
        profiles_dct_lst.append(profile_dct)
    return profiles_dct_lst


def fetch_profiles(info: dict) -> List[dict]:
    profiles_dct_lst = extract_profiles_from_db()
    matches = []
    for profile_dct in profiles_dct_lst:
        if is_sub_dict(profile_dct, info):
            matches.append(profile_dct)
    return matches


###############MAIN##############################3
"""
if __name__ == '__main__':

    #ps = create_profiles(0)
    #for p in ps:
    #    print_profile(p)
    with open('db.json', 'w+') as f:
        for pros in extract_profiles_from_db():
            print_profile(pros, f)
"""



