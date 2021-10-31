#std
from flask import Flask, redirect, url_for, request, render_template, flash, Blueprint, jsonify, session
import time

#inner project
import security
import fields

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


class Endpoints:

    def __init__(self, db_inst):
        self.db_inst = db_inst
        self.rules = self.set_rules() 
    
    def set_rules(self):
        """
        admin contains auth that can do anything

            GET /tr@ht.com   get all info , user does what they want with it | 404 bad request if not exist    *need to be signed in
            DELETE   *must be signed in, you can only aim your account " | else 404

            POST /  *post by body,  | if not complete return errors json | 404 if not exist
            PUT     *must be signed in, you can only aim your account         in body | if key dont exist or cant be changed

        """
        """to avoid request payloads, put as much info as possible in link, a msg 1000 long has to be in body"""
        #urls_root = 'http://127.0.0.1:5000'

        rules = dict()

        rules['home_page'] = {'url': '/', 'mthds': None, 'view': self.home}
        rules['sign_up'] = {'url': '/signup', 'mthds': ['GET', 'POST'], 'view': self.signup}
        rules['sign_in'] = {'url': '/signin', 'mthds': ['GET', 'POST'], 'view': self.signin}
        rules['activate_account'] = {'url': '/activate_account', 'mthds': ['GET'], 'view': self.activate_account} # ?key= token
        #manage_account = {'url': '/<email>', 'mthds': ['POST', 'PUT', 'DELETE', 'GET'], 'view': Views.account_manager}  # to search or filter
        
        

        """
        log_in = {'url': '/login/<email>', 'mthds': ['POST'], 'view': Urlrules.home_page}
        sign_in = {'url': '/logout/<email>', 'mthds': ['POST'], 'view': FN}
        sign_up = {'url': '/signup', 'mthds': ['POST'], 'view': FN}
        sign_up = {'url': '/msg/<from_email>/<to_email>', 'mthds': ['POST', 'PUT', 'DELETE', 'GET'], 'view': FN} #body must contain json 'msg' :
        sign_up = {'url': '/<email>', 'mthds': ['POST', 'PUT', 'DELETE', 'GET'], 'view': FN} #to search or filter
        sign_up = {'url': '/users', 'mthds': ['POST', 'PUT', 'DELETE', 'GET'], 'view': FN}  # to search or filter ? + -   ?filter=likes+name+birthdate
        sign_up = {'url': '/like/<from_email>/<to_email>', 'mthds': ['GET', 'PUT'], 'view': FN}
        sign_up = {'url': '/block/<from_email>/<to_email>', 'mthds': ['GET' , 'PUT'], 'view': FN}
        activate_account = {'url': '/activate/<user>/<token>', 'mthds': ['POST'], 'view': FN}
        format_activate_account = 'http://127.0.0.1:5000/matcha_activate_account/{}'

        """
        return rules


    def home(self):
        page_page_data = {'msg': 'welcome to MATCHA'}
        return jsonify(page_page_data)

    def signup(self):
        page_data = dict()
        if request.method == 'GET':
            page_data = {'msg': 'post page_page_data about yourself'}
        if request.method == 'POST':
            page_data = request.json #form.to_dict()
            page_data = security.clean_user_data(page_data)  # if key is not present ,its None, causing checkers to raise an exc.
            is_valid = fields.is_profile(page_data)
            if not is_valid:
                page_data = {'success': False, 'msg': 'error, page_page_data wrong'}
            else:
                page_data = {'success': True, 'msg': Notifications.sign_up_success}
        return jsonify(page_data)


    def signin(self):

        page_data = dict()
        if request.method == 'GET':
            page_data = {'msg': 'welcome, present your credentials'}
        if request.method == 'POST':
            page_data = request.json #form.to_dict()
            page_data = security.clean_user_page_data(page_data)  # if key is not present ,its None, causing checkers to raise an exc.        
            email = page_data['email']
            pwd = page_data['pwd']
            profile = self.db_inst.user_exists_with_pwd(email, pwd)
            if profile:
                if profile['blocked']:
                    page_data = {'msg': 'you have been blocked contact admin'}
                elif not profile['activated']:
                    page_data = {'msg': 'please activate your account threw the mail, if expired request new'}
                elif profile['signed_in']:
                    page_data = {'msg' : 'you are already signed in'}
                else:
                    self.db_inst.set_prop(email, 'signed_in','true')
                    #redirect?
            else:
                page_data = {'msg': 'pwd or login wrong'}
        return jsonify(page_data)

    #have to be loged in
    def activate_account(self):

        page_data = dict()
        if request.method == 'POST':
            page_data = request.json #form.to_dict()
            """args -> /activate_account?key= :  """
            token = page_data['token']


            #if request is get?
            res = security.get_token_page_data(token) #-> if fails returns {'email' : ''}
            #CLEAN page_data
            #CHECK DTA FORMALITY
            if res == 'expired':
                page_data = {'msg' : 'This is an invalid or expired token, please generate a new one by signing up!'}
            else:
                email = res
                self.db_inst.set_prop(email, 'signed_in','true')
                page_data = {'msg' : 'account activated!'}


        return jsonify(page_data)
        # return redirect('/')
        # redirect to users account render_template('user_main_page.html', page_data=page_data)  # the update



'''
    def modify_account(self):
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

    def send_msg(self):
        #?from_email='';to_mail=''  JSON 'msg'
        # check if demador signed in
        if request.method == 'GET':
            # get conversiation between a b
        if request.method == 'POST':
            # send json with field msg

    def toggle_like_user(self):
        # ?from_email='';to_mail='';n='-1'
        # check if demador signed in
        if request.method == 'GET':
            # get bool if you liked user
        if request.method == 'POST':
            #add n
            #add like if not not liked
            # -1 if at 1

    def toggle_block_user(self):
        # ?from_email='';to_mail='';n='-1'
        # check if demador signed in
        if request.method == 'GET':
        # get bool if blocked users
        if request.method == 'POST':
            # add n
            # add like if not not liked
            # -1 if at 1

    def ft_matcha(self):
        # ?cmp_email=''
        if request.method == 'GET':
            # get lst of users who match you with % indicator

    def filter_users(self):
        # ?ways=time='05:45:22',name=,... multiple of JSON
        if request.method == 'GET':
            #check if fields has to be one and fields are correct
            #get lst

    def unblock_user(self):
        # ?blocked_email=''
        #needs admin auth









    #def account_manager(self):
    #pass
'''
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
def urlrule_signup(self):
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






