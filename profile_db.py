"""
uses all 4 ind. mod.
"""

import random
import string

from gen_random import *
from sqlite_db import *
from dict_ops import *
from zemail import *
from security_ import *


def format_profile(profile):
    # fields not seen on sign page
    profile['blocked'] = False
    profile['activated'] = False
    profile['likes'] = []
    profile['msgs'] = []
    return profile

# db + dict_ops
def load_profiles_in_db(profiles):
    for profile_dict in profiles:
        profile_str = dict_to_str(profile_dict)
        exec_sql(Sql_cmds.insert.format('users', 'profile', profile_str))


def extract_profiles_from_db():
    users_table = exec_sql(Sql_cmds.fetch.format('users'))
    col_str = 'profile'
    profiles_dct_lst = []
    for row_nb in range(len(users_table)):
        profile_str = users_table[row_nb][col_str]
        profile_dct = str_to_dict(profile_str)
        profiles_dct_lst.append(profile_dct)
    return profiles_dct_lst

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

def fetch_profiles(info):
    #returns if equal, if more than one than not normal
    profiles_dct_lst = extract_profiles_from_db()
    matches = []
    for profile_dct in profiles_dct_lst:
        if is_sub_dict(profile_dct, info):
            matches.append(profile_dct)
    return matches

def profile_exists(info):
    # email is unik
    info_email = dict_val_similar_key(info, 'email')
    x = fetch_profiles({'email': info_email})
    return len(x) == 1


def update_profile(email, data):
    profile = fetch_profiles({'email': email})[0]
    unik_id = fetch_unikid_profile_by_email(email)
    exec_sql(Sql_cmds.delete_row.format('users', 'id', unik_id))
    profile.update(data)
    load_profiles_in_db([profile]) #will have new unik id

def block_user(email):
    update_profile(email, {'blocked':True})

def like_user(from_email, to_email):
    profile = fetch_profiles({'email': from_email})[0]
    likes = dict_val_similar_key(profile, 'like')
    likes.append(to_email)
    update_profile(from_email, {'likes': likes})


def print_profile(profile):
    top = bottom = '-' * 50
    print(top)
    for k,v in profile.items():
        print(f'<{k}>'.center(15, '*'))
        if isinstance(v, list):
            for i,e in enumerate(v):
                print(f'    {i} > {e}')
        elif isinstance(v, dict):
            for a,b in v.items():
                print(f'    {a} > {b}')
        else:
            print(f'    {v}')
    print(bottom)


if __name__ == '__main__':
    ps = create_profiles(0)
    for p in ps:
        print_profile(p)

