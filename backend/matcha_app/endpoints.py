from flask import Flask, redirect, url_for, request, render_template, flash, Blueprint, jsonify, session
import time
from matcha_app.zemail import email_activate_account
from matcha_app.profile_db import *
from matcha_app.security_ import clean_user_page_data, get_token_page_data
from matcha_app.check import profile_form_valid



domain = 'http://127.0.0.1:5000/'
json_headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}


class Notifications:

    pwd_fail = 'wrong pwd'
    email_fail = 'wrong email'
    credentials_fail = 'wrong credentials'
    signin_fail = 'your not signed in'
    is_blocked = 'your blocked, contact admin'
    token_expired = 'token is expired'
    sign_up_success = 'an email has been sent, click on the link to activate your account'

    token_sent = 'a token has be sent to you in your email.'

    alerts =   {'liked' : '{nickname} liked you',
                     'liked_back': '! {nickname} liked you back !',
                     'dislike': '{nickname} unlinked you',
                     'msg' :  '{nickname} sent you a new message',
                     'visit': '{nickname} checked out your profile',
                     'loged_in': 'welcome back {nickname}!'}

    def print_errs(errs: list):
        return '\n'.join(errs)


class Views:

    def home():
        page_page_data = {'msg': 'welcome to MATCHA'}
        return jsonify(page_page_data)

    def signup():
        page_data = dict()
        if request.method == 'GET':
            page_data = {'msg': 'post page_page_data about yourself'}
        if request.method == 'POST':
            page_data = request.json #form.to_dict()
            page_data = SecurityF.clean_user_page_page_data(page_data)  # if key is not present ,its None, causing checkers to raise an exc.
            is_valid = FieldsF.profile_form_valid(page_data)
            if not is_valid:
                page_data = {'msg': 'error, page_page_data wrong'}
            else:
                page_data = {'msg': Notifications.sign_up_success}
        return jsonify(page_data)


    def signin():

        page_data = dict()
        if request.method == 'GET':
            page_data = {'msg': 'welcome, present your credentials'}
        if request.method == 'POST':
            page_data = request.json #form.to_dict()
            page_data = SecurityF.clean_user_page_data(page_data)  # if key is not present ,its None, causing checkers to raise an exc.        
            email = page_data['email']
            pwd = page_data['pwd']
            profile = DbF.user_exists_with_pwd(email, pwd)
            if profile:
                if profile['blocked']:
                    page_data = {'msg': 'you have been blocked contact admin'}
                elif not profile['activated']:
                    page_data = {'msg': 'please activate your account threw the mail, if expired request new'}
                elif profile['signed_in']:
                    page_data = {'msg' : 'you are already signed in'}
                else:
                    DbF.set_prop(email, 'signed_in','true')
                    #redirect?
            else:
                page_data = {'msg': 'pwd or login wrong'}
        return jsonify(page_data)

    #have to be loged in
    def activate_account():

        page_data = dict()
        if request.method == 'POST':
            page_data = request.json #form.to_dict()
            """args -> /activate_account?key= :  """
            token = page_data['token']


            #if request is get?
            res = get_token_page_data(token) #-> if fails returns {'email' : ''}
            #CLEAN page_data
            #CHECK DTA FORMALITY
            if res == 'expired':
                page_data = {'msg' : 'This is an invalid or expired token, please generate a new one by signing up!'}
            else:
                email = res
                DbF.set_prop(email, 'signed_in','true')
                page_data = {'msg' : 'account activated!'}


        return jsonify(page_data)
        # return redirect('/')
        # redirect to users account render_template('user_main_page.html', page_data=page_data)  # the update



'''
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


'''







    #def account_manager():
    #pass
    """
    page_data = dict()
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
        page_data = {'status': 'error', 'msg': "email don't have an account"}

    return jsonify(page_data)
    """




"""
def urlrule_login(request):
    #if clients wants to add page_data
    elif request == 'POST':
        #clean page_data
        #check if email exists in db
        #check pwd vadility

        #if success create session
        #if fail display errors
"""

"""
def urlrule_signup():
    page_data = {'errors': False, 'sign_up_valid': False, 'form': True, 'urls': Urls.__dict__}

    if request.method == 'POST':
        profile = request.form.to_dict()
        profile = clean_user_page_data(profile) #if key is not present ,its None, causing checkers to raise an exc.
        if is_correct_profile(profile):
            profile = format_profile(profile) #add token
            load_profiles_in_db([profile])
            email_activate_account(profile)
            page_data['sign_up_valid'] = True
            page_data['form'] = False
        else:
            page_data['errors'] = True

    return render_template('sign-up.html', page_data=page_data)  # the update


@Global.app.route(Urls.activate_account, methods=['GET', 'POST'])
def activate_account(token):
    #detect who it was by token yuou gvie to user
    #token = request.args.get('token')
    email = get_token_page_data(token)
    if not profile_exists({'email': email}): #if token expired, email is empty
        return 'This is an invalid or expired URL, please generate a new one!'
    else:
        update_profile(email, {'activated': True})
        return 'account activated!'
    #return redirect('/')
    #redirect to users account render_template('user_main_page.html', page_data=page_data)  # the update

"""






