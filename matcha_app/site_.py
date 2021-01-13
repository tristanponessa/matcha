from flask import Flask, redirect, url_for, request, render_template, flash, Blueprint
import sys

#sys.path.add('matcha_app')
#from matcha_app.gen_random import *
"""
from sqlite_db import *
from dict_ops import *
from exception_handler import *
from cmp_ import *
from profile_db import *
from check import *
from security_ import *
from zemail import *
"""


#bp_site = Blueprint('site_', __name__)

#app.add_url_rule('/', 'index', index)
#url_for('find_question' ,question_id=1)
#@app.route('/questions/<int:question_id>')

class Urls:

    root = 'http://127.0.0.1:5000'
    index = '/'
    sign_in = '/sign_in'
    sign_up = '/sign_up'
    profile_page = '/user_page/<user>'
    activate_account = '/activate/<user>/<token>'
    format_activate_account = 'http://127.0.0.1:5000/matcha_activate_account/{}'



def urlrule_home_page():
    return 'Hi'

"""
app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/other', view_func=views.other)
"""
"""
@bp_site.route('/')
def home_page():
    return 'Hi'



@bp_site.route('/log_in', methods=['GET', 'POST'])
def login(request):
    #if clients wants to add data
    elif request == 'POST':
        #clean data
        #check if email exists in db
        #check pwd vadility

        #if success create session
        #if fail display errors



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







