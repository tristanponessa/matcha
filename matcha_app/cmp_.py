from dict_ops import *
from profile_db import *

import sys
import inspect

def get_all_cmp_funs():
    check_funs = {}
    cur_file_members = inspect.getmembers(sys.modules[__name__])
    for member in cur_file_members:
        member_name, member_val = member
        if member_name.startswith('cmp_'):
            check_funs[member_name] = member_val
    return check_funs
########################################################################################3
def cmp_birthdate(b1, b2):
    year1 = b1.split('/')[-1]
    year2 = b2.split('/')[-1]
    return abs(year1 - year2) <= 5

def cmp_sex_orientation(pref1, gender1, pref2, gender2):
    return gender1 in pref2 and gender2 in pref1

def cmp_tags(v1, v2):
    return len(set(v1) & set(v2)) > 0 #intersection keep all eq

def cmp_location(v1, v2):
    return v1 == v2

def ccmp_profiles(pro_dct1, pro_dct2):
    sim_keys = ('tags', 'location', 'sex_orientation', 'birthdate')
    cmp_funs = get_all_cmp_funs()
    score = 0
    for sim_key in sim_keys:
        vd1 = dict_val_similar_key(pro_dct1, sim_key)
        vd2 = dict_val_similar_key(pro_dct2, sim_key)
        cmp_fun = dict_val_similar_key(cmp_funs, sim_key)
        if cmp_fun:
            score += 100 // len(sim_keys)
    e1 = dict_val_similar_key(pro_dct1, 'email')
    e2 = dict_val_similar_key(pro_dct2, 'email')
    return {'from_email': e1, 'to_email': e2, 'score': score}

def ft_matcha(from_email):
    #find profiles with at least 50 same
    prof_dct_lst = extract_profiles_from_db()
    from_prof_dct = fetch_profiles({'email': from_email})[0]
    prof_dct_lst.remove(from_prof_dct)

    matchas = []
    for prof_dct in prof_dct_lst:
        cmp = ccmp_profiles(from_prof_dct, prof_dct)
        if cmp['score'] >= 50:
            matchas.append(cmp)
    return matchas



