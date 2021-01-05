"""

or in debug mode , the reloader reloads flask when any change done ,
which means rerunning main
"""

from flask import Flask, redirect, url_for, request, render_template, flash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

import sys

from gen_random import *
from sqlite_db import *
from dict_ops import *
from exception_handler import *
from profile_db import *
from check import *
from security_ import *
from zemail import *
import string

"""
def gen_site_secret_key():
    #for hackers, default seed is the current time....
    all_ = string.ascii_letters + string.digits + "!#$%&()*+,-./:;<=>?@[]^_{|}~"
    rpwd = ''.join((random.choice(all_) for _ in range(random.randint(64, 128))))
    return (rpwd)
"""

class Global:
    app = Flask(__name__)
    #SITE_SECRET_KEY = gen_site_secret_key()


class Urls:

    root = 'http://127.0.0.1:5000'
    index = '/'
    sign_in = '/sign_in'
    sign_up = '/sign_up'
    profile_page = '/<string>_profile_page/'
    activate_account = '/matcha_activate_account/<token>'
    format_activate_account = 'http://127.0.0.1:5000/matcha_activate_account/{}'






def start_web_app():
    Global.app.use_reloader = False
    Global.app.secret_key = 'super secret'
    Global.app.run(debug=False)


def main(argv):
    #prepare db
    master_seed = 0 if len(argv) != 2 else int(argv[1])
    if os.path.exists('matcha.db'):
        os.remove('matcha.db')
    init_db()
    profiles = gen_random_profiles(master_seed)
    load_profiles_in_db(profiles)
    #start site
    start_web_app()#synchronous, anythin after wont be run until this done

    #except Exception:
    #    print(get_exception())
    #finally:



@Global.app.route(Urls.index)
def main_page():
    return render_template('index.html', urls_lst=Urls.__dict__) #the update


@Global.app.route(Urls.sign_up, methods=['GET', 'POST'])
def signup_controler():
    data = {'errors': False, 'sign_up_valid': False, 'form': True, 'urls': Urls.__dict__}

    if request.method == 'POST':
        profile = request.form.to_dict()
        profile = clean_user_data(profile) #if key is not present ,its None, causing checkers to raise an exc.
        if is_correct_profile(profile):
            profile = format_profile(profile) #add token
            load_profiles_in_db([profile])
            email_activate_account(profile)
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



@Global.app.route(Urls.activate_account, methods=['GET', 'POST'])
def activate_account(token):
    #detect who it was by token yuou gvie to user
    #token = request.args.get('token')
    email = get_token_data(token)
    if not profile_exists({'email': email}): #if token expired, email is empty
        return 'This is an invalid or expired URL, please generate a new one!'
    else:
        """
        profile = fetch_profiles(email)
        profile['activated'] = True
        load_profiles_in_db([profile])
        """
        update_profile(email, {'activated': True})
        return 'account activated!'
    #return redirect('/')
    #redirect to users account render_template('user_main_page.html', data=data)  # the update



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