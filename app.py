import os
from flask import Flask
from dotenv import load_dotenv

from matcha_app.site_ import bp_site


def load_env():
    basedir = os.path.abspath(os.path.dirname(__file__))
    p = os.path.join(basedir, '.env')
    load_dotenv(dotenv_path=p)


def launch_flask():
    app = Flask(__name__)
    app.config.from_object(os.environ.get('FLASK_ENV'))
    app.register_blueprint(bp_site)
    app.run(debug=True) #code stops here until done


if __name__ == '__main__':
    load_env()
    launch_flask()




