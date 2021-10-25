import sys
import time
import json
#sys.path.append('/home/user/Documents/coding/matcha')
#sys.path.append('/home/user/Documents/coding/matcha/matcha_app')
#sys.path.append('/home/user/Documents/coding/matcha/matcha_app/db_files')

import neo4j
from neo4j import GraphDatabase as neo4j_db

from exception_handler import get_exception

#------------------------------------#------------------------------------#------------------------------------#------------------------------------#------------------------------------



#users must choose fomr this list  the subject demands they're "reusable". I interpret this as an object you use and not just a plain data



class Db:

    """
        *session.runs returns a list of dicts of key:str value:dict [{'cql return name': {}},
                                                                     {'cql return name': {}} ...]
        *__var activates pythons name mangling, means private, dont call outside class
        *1.string format prints brackets for {v} -> {key:val,...} when v is a dict, 
            otherwise {{v}} -> {v}  {{}} -> {}
         2.
        *all data checked before being used threw db
        *cql: 
            ' is a syntax error use "
            merge updates existing (if exists,updates,else creates)
            create will duplicate if exists
            WITH allows you to chain MERGE in the middle of an espr
        *driver.session.read/write_transaction are the best fns, they auto-commit and roll-back when necessary
         tx represents with begin_transaction() as tx: in the doc, i dont know where its called 
        *neo4j.work.result.Result contains multiple neo4j.Record
         be careful, record in result moves all outside, reaccessing result gives you an empty lst, i think it calls consume()
    """

    def __init__(self, uri, userName, password):
        self._driver = None
        self.err_msgs = []
        
        self.try_connection(uri, userName, password)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._driver:
            self.close_db()
        
    def try_connection(self,uri, userName, password):
        #driver is set even if an exception happens, closed, the true test is a cmd run
        try:
            self._driver = neo4j_db.driver(uri, auth=(userName, password))
            self._run_cmd('MATCH (n) RETURN n') #will cause the exceptions
            return True
        except neo4j.exceptions.ServiceUnavailable:
            #normally except ConnectionRefusedError: is raised but is jumpred now i catch this for some reason
            self.err_msgs.append(get_exception("DATABASE NOT ACTIVE"))
        except neo4j.exceptions.AuthError:
            self.err_msgs.append(get_exception("WRONG CREDENTIALS"))
        except Exception:
            self.err_msgs.append(get_exception())
        
        if len(self.err_msgs) > 0:
            self._driver = None

    def close_db(self):
        self._driver.close()
        
    
    def _run_cmd(self, cmd, return_type=''):
        with self._driver.session() as session:
            result_obj =  session.run(cmd)
            result = self.db_result_format(result_obj, return_type)
            #result = result_obj.data() #lst of dcts
            return result

    def _timestamp(self):
        epoch_now = time.time()
        structtime_now = time.localtime(epoch_now)
        format_now = time.strftime("%Y-%m-%d %H:%M:%S", structtime_now)
        return format_now
    
    def _cql_formater(self, d: dict):
        #1.converts str to cql types for correct sorting/filtering
        #neo4j proposes a format string with $var instead of {}
        #2.{'name':'val'} converts to -> {name:'val'}
        
        d['birthdate'] = self._cql_type('date', d['birthdate'])
        #if k == 'date':
            #v = self._cql_type('timestamp', v)

        dstr = json.dumps(d) #json transforms ' to "
        for k in d.keys():
            dstr = dstr.replace(f'"{k}"', k)
        return dstr
    
    def _cql_type(self, type, data):
        if type == 'date':
            return f"date('{data}')"
        
    
    def db_result_format(self, res_obj, return_type=''):
        #session.runs returns a list of dicts [{'cql return name': {'key1','val1'}, ...]
        #we trasform into      list of dicts  [{'key1','val1'}]
        r = None
        if return_type == '':
            r = [list(dct.values())[0] for dct in res_obj]
        elif return_type == 'len':
            r = len(res_obj.data())
        elif return_type == 'values':
            pass
        elif return_type == 'object':
            r = res_obj
        return r
    
    def dbres_get(self, r, index, prop=None):
        #[{'dct1_key1':1,'prop':2,...},  {'dct2_key1':0}]
        dct = r[index] if index < len(r) else None
        return dct.get(prop) if prop else dct

    def cql_set_users(self, props, data):
        props = self._cql_formater(props)
        cql_cmd = f'''
                    MATCH (p{props})
                    SET p += '{data}'
                    RETURN p
                  '''
        return cql_cmd
    
    def cql_get_users(self, props, order='+', order_prop='email'):
        order = 'ASC' if order == '+' else 'DESC' #('DESC','ASC')[order=='+']
        props = self._cql_formater(props)
        cql_cmd = f'''
                    MATCH (p{props})
                    RETURN p
                    ORDER BY p.{order_prop} {order}
                  '''
        return cql_cmd
    
    def cql_create_user(self, props):
        props = self._cql_formater(props)
        cql_cmd = f'''
                    CREATE (p{props})
                    RETURN p
                  '''
        return cql_cmd

    def cql_delete_user(self, props):
        props = self._cql_formater(props)
        cql_cmd = f'''
                    MATCH (p{props})
                    DELETE p
                  '''
        return cql_cmd


    


    #def profiles_to_db(pros):

            