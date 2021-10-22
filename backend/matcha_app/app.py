from flask import Flask, redirect, url_for, request, render_template, flash
import time
from flask import Flask
from dotenv import load_dotenv
import sys
from inspect import getmembers, isfunction
from flask import Flask, redirect, url_for, request, render_template, flash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

app = Flask(__name__)

def start_web_app():
    Global.app.use_reloader = False
    Global.app.secret_key = 'super secret'
    Global.app.run(debug=False)









def load_env():
    basedir = os.path.abspath(os.path.dirname(__file__))
    p = os.path.join(basedir, '.env')
    load_dotenv(dotenv_path=p)

def add_url_rules(app):
     for name,v in UrlRules.get_cls_data().items():
        app.add_url_rule(v['url'], methods=v['mthds'], view_func=v['view'])


def launch_flask():
    #load_env()
    app = Flask(__name__)
    app.config.from_object(os.environ.get('FLASK_ENV'))
    add_url_rules(app)
    setup_db()
    #app.register_blueprint(bp_site)
    app.use_reloader = False #proforms double db actions and problems
    app.run(debug=True) #code stops here until done


if __name__ == '__main__':
    launch_flask()