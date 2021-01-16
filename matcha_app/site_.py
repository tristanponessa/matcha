from flask import Flask, redirect, url_for, request, render_template, flash, Blueprint, jsonify

from matcha_app.zemail import email_activate_account
from matcha_app.profile_db import format_profile, load_profiles_in_db, profile_exists, update_profile
from matcha_app.security_ import clean_user_data, get_token_data
from matcha_app.check import is_correct_profile

#bp_site = Blueprint('site_', __name__)
#app.add_url_rule('/', 'index', index)
#url_for('find_question' ,question_id=1)
#@app.route('/questions/<int:question_id>')

class Views:


    def home():
        return 'Hi'


    def signup():

        data = dict()
        if request.method == 'GET':
            data = {'state' : 'get_form', 'fields':['email','pwd']}
        if request.method == 'POST':
            data = request.json #form.to_dict()
            data = clean_user_data(data)  # if key is not present ,its None, causing checkers to raise an exc.
            if is_correct_profile(data):
                profile = format_profile(data)  # add token
                load_profiles_in_db([profile])
                email_activate_account(profile)
                data = {'state': 'success', 'msg': 'email sent to you, activate account'}
            else:
                data = {'state': 'error', 'email':'email must be', 'pwd' : 'must be'}
        return jsonify(data)

    #have to be loged in
    def activate_account():
        """args -> /activate_account?key= :  """
        token = request.args.get('key') #fails return None
        data = dict()

        email = get_token_data(token) #-> if fails returns {'email' : ''}
        if not profile_exists({'email': email}):  # if token expired, email is empty
            data = {'msg' : 'This is an invalid or expired URL, please generate a new one!'}
        else:
            #i have no fn idea but maybe theres a hack if no protection but everythings is hackable
            update_profile(email, {'activated': True})
            data = {'state': 'success', 'msg' : 'account activated!'}

        return jsonify(data)
        # return redirect('/')
        # redirect to users account render_template('user_main_page.html', data=data)  # the update




class UrlRules:
    """
      admin contains auth that can do anything

          GET /tr@ht.com   get all info , user does what they want with it | 404 bad request if not exist    *need to be signed in
          DELETE   *must be signed in, you can only aim your account " | else 404

          POST /  *post by body,  | if not complete return errors json | 404 if not exist
          PUT     *must be signed in, you can only aim your account         in body | if key dont exist or cant be changed

    """
    """to avoid request payloads, put as much info as possible in link, a msg 1000 long has to be in body"""
    #urls_root = 'http://127.0.0.1:5000'

    home_page = {'url': '/', 'mthds': None, 'view': Views.home}
    sign_up = {'url': '/signup', 'mthds': ['GET', 'POST'], 'view': Views.signup}
    activate_account = {'url': '/activate_account', 'mthds': ['GET'], 'view': Views.activate_account} # ?key=
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

    @staticmethod
    def get_cls_data():
        return {k: v for k, v in UrlRules.__dict__.items() if isinstance(v, dict)}



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






