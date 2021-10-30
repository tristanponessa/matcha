#builtin
import time
import sys
from inspect import getmembers, isfunction
#3rd party
from flask import Flask, redirect, url_for, request, render_template, flash
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#inner project 
import endpoints
import db


def add_url_rules(app):
     for name,v in endpoints.get_cls_data().items():
        app.add_url_rule(v['url'], methods=v['mthds'], view_func=v['view'])

def launch_flask(uri, userName, password):
    with db.Db(uri, userName, password) as db_inst:

        if len(db_inst.err_msgs) > 0:
            print(*db_inst.err_msgs, sep='\n')
            return

        app = Flask(__name__)
        add_url_rules(app)
        app.use_reloader = False #proforms double db actions and problems
        app.run(debug=True) #code stops here until done


if __name__ == '__main__':
    #sys.argv  env=test,release, dbinfo=
    launch_flask()