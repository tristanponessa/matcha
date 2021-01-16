import os
import time
from flask import Flask
from dotenv import load_dotenv
import sys
from inspect import getmembers, isfunction
#from matcha_app.site_ import bp_site
from matcha_app.site_ import UrlRules
from matcha_app.sqlite_db import init_db
from matcha_app.profile_db import load_profiles_in_db
from matcha_app.gen_random import create_profiles
from matcha_app.utils import if_file_del

def load_env():
    basedir = os.path.abspath(os.path.dirname(__file__))
    p = os.path.join(basedir, '.env')
    load_dotenv(dotenv_path=p)

def add_url_rules(app):
     for name,v in UrlRules.get_cls_data().items():
        app.add_url_rule(v['url'], methods=v['mthds'], view_func=v['view'])

def setup_db():
    if_file_del('./matcha.db')
    init_db()
    profiles = create_profiles(0)
    load_profiles_in_db(profiles)

def launch_flask():
    load_env()
    app = Flask(__name__)
    app.config.from_object(os.environ.get('FLASK_ENV'))
    add_url_rules(app)
    setup_db()
    #app.register_blueprint(bp_site)
    app.use_reloader = False
    app.run(debug=False) #code stops here until done


if __name__ == '__main__':
    launch_flask()




