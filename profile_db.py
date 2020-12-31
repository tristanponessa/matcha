"""
uses all 4 ind. mod.
"""

import random
import string

from gen_random import *
from sqlite_db import *
from dict_ops import *

def load_profiles_in_db(profiles, cur): #random + db + dict_ops
    for profile_dict in profiles:
        profile_str = dict_to_str(profile_dict)
        #print(Sql_cmds.insert.format('users', 'profile', profile_str))
        exec_sql(cur, Sql_cmds.insert.format('users', 'profile', profile_str))
        
def extract_profiles_from_db(cur):
    users_table = exec_sql(cur, Sql_cmds.fetch.format('users'))
    col_str = 'profile'
    profiles_dct_lst = []
    for row_nb in range(len(users_table)):
        profile_str = users_table[row_nb][col_str]
        profile_dct = str_to_dict(profile_str)
        profiles_dct_lst.append(profile_dct)
    return profiles_dct_lst

def fetch_profiles(cur, info):
    profiles_dct_lst = extract_profiles_from_db(cur)
    matches = []
    for profile_dct in profiles_dct_lst:
        if is_sub_dict(profile_dct, info):
            matches.append(profile_dct)
    return matches

def profile_exists(cur, info):
    #email is unik
    info_email = dict_val_similar_key(info, 'email')
    x = fetch_profiles(cur, {'email' : info_email})
    return len(x) == 1


    
    


"""
#overkill function? 
def gen_rand_profiles_AND_load_in_db(cur, master_seed): #fusion of 2 funs
    profiles = gen_random_profiles(master_seed)
    load_profiles_in_db(profiles, cur)

if __name__ == '__main__':
    db_manager()
    gen_rand_profiles_AND_load_in_db(,0)
"""