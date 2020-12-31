import sys

from gen_random import *
from sqlite_db import *
from dict_ops import *

from exception_handler import *
from profile_db import *

def main(argv):

    master_seed = 0 if len(argv) != 2 else int(argv[1])
    conn,cur = None,None
    try:
        conn, cur = db_conn()
        init_db(conn, cur)
        profiles = gen_random_profiles(master_seed)
        load_profiles_in_db(profiles, cur)

    
    except Exception as e:
        print(get_exception())
    finally:
        db_close(conn, cur)


def sign_up(cur, info):
    #check info
    load_profiles_in_db([info], cur)
    
    #redirect to profile main page
    #check 




if __name__ == '__main__':
    main(sys.argv)






#fetch tests
"""
x = fetch_profiles(cur, {"email": "NSWP@gmail.com"})
print(len(x))
x = fetch_profiles(cur, {"birthdate": "NSWP@gmail.com"})
print(len(x))

for i in range(10000):
    x = fetch_profiles(cur, {"birthdate": "17/03/1995"})
    print(len(x))




      #on click on sign up, add this to the fields that posts a dict
        post_info = {"gen_random_firstname": "TRIS_Hreltpus", "gen_random_lastname": "Hreltpusctapi", "gen_random_profilepic": "./pics/c.png", "gen_random_pics": ["./pics/python-qhd-3840x2400.jpg"], "gen_random_email": "LIixMEOL123456@hotmail.com", "gen_random_pwd": "^>qV{+~]i{b+H?Dy+>?+Y0t", "gen_random_birthdate": "8/10/1989", "get_random_sexori": "straight"}
        sign_up(cur, post_info)
        print('sign up sucess? ', profile_exists(cur, post_info))

def sign_in(info):
    #check if user present , if so check pwd
    #info must have post email pwd
    if not profile_exists():
        return #launch sign up  , ask front to display you dont have n account
    #start session
    #return succeeded to front to change url to display profile

    #deal with blocked profiles -> if blocked display youve been blocked page contact adm

"""