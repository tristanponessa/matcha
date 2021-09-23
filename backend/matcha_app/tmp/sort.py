from profile_db import *

def sort_profiles(key):

#
def filter_profiles(info):
    return fetch_profiles(info)


   #returns if equal, if more than one than not normal
    profiles_dct_lst = extract_profiles_from_db()
    matches = []
    for profile_dct in profiles_dct_lst:
        if is_sub_dict(profile_dct, info):
            matches.append(profile_dct)
    return matches

def ft_matcha(cmp_from_email):
    #must recalc everytime in case someone changes stats
    cmp_profile = fetch_profiles({'email': cmp_from_email})[0]
    profiles_dct_lst = extract_profiles_from_db()

    #not itself
    matchas = [] {'perc' : 75}
    for pro_dct in profiles_dct_lst:


    #perc calc if 5 equal keys 75 7 or more 95
