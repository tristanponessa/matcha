"""
uses all 4 ind. mod.
"""

import random
import string
from typing import List
from matcha_app.gen_random import *
from matcha_app.sqlite_db import *
from matcha_app.dict_ops import *
from matcha_app.zemail import *
from matcha_app.security_ import *

"""
class ProfileInfo:
    
    keys = [
                'names' : ['activated', ] , ''
        
            ]
            
            visible_to = ('public', ')
keys_visibility = {
    'first_name': visible_to
    'last_name': visible_to
    'location':
    'msgs' 
    'likes'
    'pics'
    'birthdate'
    'gender':
    'tags':
    'intro':
    'signed_in'
    'blocked'
    'activated': ['']
    'pwd' : ['admin']
"""






# db + dict_ops

#DB ACTION
def load_profiles_in_db(profiles) -> None:
    for profile_dict in profiles:
        profile_str = dict_to_str(profile_dict)
        exec_sql(Sql_cmds.insert.format('users', 'profile', profile_str))

def update_profile(email, data):
    profile = fetch_profiles({'email': email})[0]
    unik_id = fetch_unikid_profile_by_email(email)
    exec_sql(Sql_cmds.delete_row.format('users', 'id', unik_id))
    profile.update(data)
    load_profiles_in_db([profile]) #will have new unik id

#CHECK FUNS
def profile_get(email, key):
    return fetch_profiles({'email': email})[0][key]


def profile_exists(email, fetch=False):
    x = fetch_profiles({'email': email})
    if fetch:
        return x
    return len(x) == 1
    #return len(fetch_profiles({'email': email})) == 1


def is_profile_signedIn(email):
    return fetch_profiles({'email': email})[0]['signed_in']

#GET FUNS
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


#MODIFY FUNS
#def block_user(email):
#    update_profile(email, {'blocked':True})

def like_user(from_email, to_email):
    profile = fetch_profiles({'email': from_email})[0]
    #likes = dict_val_similar_key(profile, 'like')
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

#DISPLAY FUNS
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

if __name__ == '__main__':
    ps = create_profiles(0)
    for p in ps:
        print_profile(p)

