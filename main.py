from flask import Flask, redirect, url_for, request, render_template

import sys

from gen_random import *
from sqlite_db import *
from dict_ops import *
from exception_handler import *
from profile_db import *
from check import *


class Global:
    conn, cur = None, None
    app = Flask(__name__)


class Urls:

    index = '/'
    sign_in = '/sign_in'
    sign_up = '/sign_up'
    profile_page = '/<string>_profile_page/'


def start_web_app():
    Global.app.run(debug=True)


def main(argv):

    master_seed = 0 if len(argv) != 2 else int(argv[1])
    try:
        Global.conn, Global.cur = db_conn()
        init_db(Global.conn, Global.cur)
        profiles = gen_random_profiles(master_seed)
        load_profiles_in_db(profiles, Global.cur)
        start_web_app()

    except Exception:
        print(get_exception())
    finally:
        db_close(Global.conn, Global.cur)


@Global.app.route(Urls.index)
def main_page():
    return render_template('index.html', urls_lst=Urls.__dict__) #the update


@Global.app.route(Urls.sign_up, methods=['GET', 'POST'])
def signup_controler():
    data = {'errors': False, 'sign_up_valid': False, 'form': True}
    if request.method == 'POST':
        profile = request.form
        for k,v in profile.values():
            print(k,':',v)
        if is_correct_profile(profile):
            load_profiles_in_db([profile], Global.cur)
            #send email
            data['sign_up_valid'] = True
            data['form'] = False
        else:
            data['errors'] = True
    return render_template('sign-up.html', data=data)  # the update

        #get post data
        #clean post data
        #check post data

        #if good
            #save in db

        # redirect update view with user main page or click on link
            # if bad
        # update with error messages on same page

        #get post data
        #clean post data
        #check post data

        #if good
            #save in db
            #redirect update view with user main page or click on link
        #if bad
            #update with error messages on same page


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