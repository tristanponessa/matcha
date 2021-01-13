#html <button form  action=python controller()>
from flask import request

from gen_random import *
from sqlite_db import *
from dict_ops import *

from exception_handler import *
from profile_db import *

app = Flask(__name__)
app.run(debug=True)


@app.route('/admin')
def hello_admin():
   return 'Hello Admin'


def signup_controler():
   if request.method == 'POST':
       profile = request.form
       if is_correct_profile(profile):
           load_profiles_in_db(profile)
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



