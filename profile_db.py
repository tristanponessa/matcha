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
        exec_sql(cur, Sql_cmds.insert.format('users', 'profile', profile_str))

def fetch_profile(cur, info)
    users_table = exec_sql(cur, Sql_cmds.fetch.format('users'))
    col = 'profile'
    profiles_dct_lst = (str_to_dict(profile_str) for profile_str in users_table[col])

    

    
    


"""
#overkill function? 
def gen_rand_profiles_AND_load_in_db(cur, master_seed): #fusion of 2 funs
    profiles = gen_random_profiles(master_seed)
    load_profiles_in_db(profiles, cur)

if __name__ == '__main__':
    db_manager()
    gen_rand_profiles_AND_load_in_db(,0)
"""