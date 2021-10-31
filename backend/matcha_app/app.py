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

class App:

    def __init__(self, uri, userName, password):
        self.db_inst = None
        self.endpoints_obj = None
        self.app_obj = None

        self.setup_flask(uri, userName, password)

    def add_url_rules(self, app, endpoints_obj):
        for name,v in endpoints_obj.rules.items():
            app.add_url_rule(v['url'], methods=v['mthds'], view_func=v['view'])

    def setup_flask(self, uri, userName, password):
        with db.Db(uri, userName, password) as db_inst:

            if len(db_inst.err_msgs) > 0:
                print(*db_inst.err_msgs, sep='\n')
                return
            
            self.db_inst = db_inst
            self.endpoints_obj = endpoints.Endpoints(db_inst)

            self.app_obj = Flask(__name__)
            self.add_url_rules(self.app_obj, self.endpoints_obj)
            

    def launch_flask(self):
            self.app.run(debug=False, use_reloader=False) #code stops here until done    #proforms double db actions and problems


if __name__ == '__main__':
    #sys.argv  env=test,release, dbinfo=
    try:
        uri =  sys.argv[1]
        host = sys.argv[2]
        pwd = sys.argv[3]
    except IndexError:
        uri, host, pwd = ('bolt://localhost:7687', 'neo4j', '0000')
        
    app = App(uri, host, pwd)
    app.launch_flask()