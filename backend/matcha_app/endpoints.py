from flask import Flask, redirect, url_for, request, render_template, flash, Blueprint, jsonify, session
import time
from matcha_app.zemail import email_activate_account
from matcha_app.profile_db import *
from matcha_app.security_ import clean_user_data, get_token_data
from matcha_app.check import profile_form_valid



domain = 'http://127.0.0.1:5000/'
json_headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

#bp_site = Blueprint('site_', __name__)
#app.add_url_rule('/', 'index', index)
#url_for('find_question' ,question_id=1)
#@app.route('/questions/<int:question_id>')
class Notifications:

    pwd = 'wrong pwd'
    email = 'wrong email'
    credentials = 'wrong credentials'
    signin = 'your not signed in'
    blocked = 'your blocked, contact admin'
    token = 'token is expired'

    token_sent = 'a token has be sent to you in your email.'

    notifications = {'liked' : '{nickname} liked you',
                     'liked_back': '! {nickname} liked you back !',
                     'dislike': '{nickname} unlinked you',
                     'msg' :  '{nickname} sent you a new message',
                     'visit': '{nickname} checked out your profile',
                     'loged_in': 'welcome back {nickname}!'}


    def print_errs(errs: list):
        return '\n'.join(errs)


class Views:


    def home():
        return 'Hi'


    def signup():

        data = dict()
        if request.method == 'GET':
            data = {'state' : 'get_form', 'fields':['email','pwd', 'name','location']}
        if request.method == 'POST':
            data = request.json #form.to_dict()
            data = clean_user_data(data)  # if key is not present ,its None, causing checkers to raise an exc.
            if profile_form_valid(data):

                def x(data):
                    fprofile = format_profile(data)
                    load_profiles_in_db([fprofile])
                    email_activate_account(fprofile)
                    data = {'state': 'success', 'msg': 'email sent to you, activate account'}

                profile = profile_exists(data['email'], True)
                if profile:
                    if not profile['activated']:
                        del_profile(data['email'])
                        time.sleep(1)
                        x(data)
                    else:
                       data = {'msg': 'email already taken'}
                else:
                    x(data)
            else:
                data = {'state': 'error', 'email':'email must be', 'pwd' : 'must be'}
        return jsonify(data)


    def signin():

        data = dict()
        if request.method == 'GET':
            data = {'state' : 'get_form', 'fields':['email','pwd']}
        if request.method == 'POST':


            data = request.json #form.to_dict()
            data = clean_user_data(data)  # if key is not present ,its None, causing checkers to raise an exc.

            #!!fetch profiles called 3 times profomrance issue?
            #check profile exists
            #profile = None


            profile = profile_exists(data['email'], True)
            print()
            if profile and data['pwd'] == profile['pwd']:
                if profile['blocked']:
                    data = {'msg': 'you have been blocked contact admin'}
                elif not profile['activated']:
                    data = {'msg': 'please activate your account threw the mail, if expired request new'}
                elif profile['signed_in']:
                    data = {'msg' : 'you are already signed in'}
                else:
                    update_profile(data['email'], {'signed_in' : True})
            else:
                data = {'msg': 'pwd or login wrong'}

        return jsonify(data)

    #have to be loged in
    def activate_account():

        data = dict()
        if request.method == 'GET':

            """args -> /activate_account?key= :  """
            token = request.args.get('key') #fails return None


            #if request is get?
            res = get_token_data(token) #-> if fails returns {'email' : ''}
            #CLEAN DATA
            #CHECK DTA FORMALITY
            if res == 'expired':
                data = {'msg' : 'This is an invalid or expired token, please generate a new one by signing up!'}
            else:
                email = res
                update_profile(email, {'activated': True})
                data = {'state': 'success', 'msg' : 'account activated!'}


        return jsonify(data)
        # return redirect('/')
        # redirect to users account render_template('user_main_page.html', data=data)  # the update

    def modify_account():
        #?email=''
        # check if demador signed in
        if all(()):
            return jsonify({''})

        if request.method == 'GET':
            #get modifiable user fields dict + get profile from db
        if request.method == 'POST':
            #aiming himself
            #dont have to put ll fields,
        if request.method == 'DELETE':
            #aiming himself

    def send_msg():
        #?from_email='';to_mail=''  JSON 'msg'
        # check if demador signed in
        if request.method == 'GET':
            # get conversiation between a b
        if request.method == 'POST':
            # send json with field msg

    def toggle_like_user():
        # ?from_email='';to_mail='';n='-1'
        # check if demador signed in
        if request.method == 'GET':
            # get bool if you liked user
        if request.method == 'POST':
            #add n
            #add like if not not liked
            # -1 if at 1

    def toggle_block_user():
        # ?from_email='';to_mail='';n='-1'
        # check if demador signed in
        if request.method == 'GET':
        # get bool if blocked users
        if request.method == 'POST':
            # add n
            # add like if not not liked
            # -1 if at 1

    def ft_matcha():
        # ?cmp_email=''
        if request.method == 'GET':
            # get lst of users who match you with % indicator

    def filter_users():
        # ?ways=time='05:45:22',name=,... multiple of JSON
        if request.method == 'GET':
            #check if fields has to be one and fields are correct
            #get lst

    def unblock_user():
        # ?blocked_email=''
        #needs admin auth










    #def account_manager():
    #pass
    """
    data = dict()
    email = request.path.split('/')[-1]

    # NEEDS TO BE SIGNED IN
    if profile_exists(email) and is_profile_signedIn(email):
        if request.method == 'GET':
            profile = fetch_profiles({'email': email})[0]

        #ALL 3
        # NEEDS TO BE SIGNED IN
        # NEEDS AUTH
        # NEEDS TO BE HIS OWN
        if
            if request.method == 'POST':
            if request.method == 'PUT':
            if request.method == 'DELETE':

    else:
        data = {'status': 'error', 'msg': "email don't have an account"}

    return jsonify(data)
    """

    def save_db_to_file():
        if request.method == 'GET':
            with open('db.json', 'w+') as f:
                for pros in extract_profiles_from_db():
                    print_profile(pros, f)
        return jsonify({'msg': 'saved to file'})



"""
def urlrule_login(request):
    #if clients wants to add data
    elif request == 'POST':
        #clean data
        #check if email exists in db
        #check pwd vadility

        #if success create session
        #if fail display errors
"""

"""
def urlrule_signup():
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


@Global.app.route(Urls.activate_account, methods=['GET', 'POST'])
def activate_account(token):
    #detect who it was by token yuou gvie to user
    #token = request.args.get('token')
    email = get_token_data(token)
    if not profile_exists({'email': email}): #if token expired, email is empty
        return 'This is an invalid or expired URL, please generate a new one!'
    else:
        update_profile(email, {'activated': True})
        return 'account activated!'
    #return redirect('/')
    #redirect to users account render_template('user_main_page.html', data=data)  # the update

"""






