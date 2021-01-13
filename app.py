import os
from flask import Flask
from dotenv import load_dotenv
import sys
from inspect import getmembers, isfunction
#from matcha_app.site_ import bp_site
import matcha_app.site_

def load_env():
    basedir = os.path.abspath(os.path.dirname(__file__))
    p = os.path.join(basedir, '.env')
    load_dotenv(dotenv_path=p)



def add_url_rules(app):
     fns_lst = getmembers(matcha_app.site_, isfunction)
     fns_dct = {tpl[0]:tpl[1] for tpl in fns_lst if tpl[0].startswith('urlrule_')}
     urls = []
     for url,fn_obj in zip(urls, fns_dct.values()):
         app.add_url_rule(url, view_func=fn_obj)

    #get all funs names with url_
    #app.add_url_rule('/index/', view_func=x.urlrule_home_page)
    app.add_url_rule('/index/', view_func=x.urlrule_home_page)

def launch_flask():
    load_env()
    app = Flask(__name__)
    app.config.from_object(os.environ.get('FLASK_ENV'))
    add_url_rules(app)
    #app.register_blueprint(bp_site)

    app.run(debug=True) #code stops here until done


if __name__ == '__main__':

    launch_flask()




