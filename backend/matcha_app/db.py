import sys
import time
import json
#sys.path.append('/home/user/Documents/coding/matcha')
#sys.path.append('/home/user/Documents/coding/matcha/matcha_app')
#sys.path.append('/home/user/Documents/coding/matcha/matcha_app/db_files')

import neo4j
from neo4j import GraphDatabase as neo4j_db



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
        self._driver = neo4j_db.driver(uri, auth=(userName, password))
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._driver:
            self.close_db()
        
            
    def close_db(self):
        self._driver.close()
        
    
    def _run_cmd(self, cmd):
        with self._driver.session() as session:
            result_obj =  session.run(cmd)
            result = result_obj.data() #lst of dcts
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
        
    
    def db_result_format(self, res):
        #session.runs returns a list of dicts [{'cql return name': {'key1','val1'}, ...]
        #we trasform into      list of dicts  [{'key1','val1'}]
        r = [list(dct.values())[0] for dct in res]
        return r if len(r) > 0 else None
    
    def dbres_get(self, r, index, prop=None):
        #[{'dct1_key1':1,'prop':2,...},  {'dct2_key1':0}]
        dct = r[index] if index < len(r) else None
        return dct.get(prop) if prop else dct

    def set_users(self, props, data):
        props = self._cql_formater(props)
        cql_cmd = f'''
                    MATCH (p{props})
                    SET p += '{data}'
                    RETURN p
                  '''
        res = self._run_cmd(cql_cmd)
        return res
    
    def get_users(self, props, order='+', order_prop='email'):
        order = 'ASC' if order == '+' else 'DESC' #('DESC','ASC')[order=='+']
        props = self._cql_formater(props)
        cql_cmd = f'''
                    MATCH (p{props})
                    RETURN p
                    ORDER BY p.{order_prop} {order}
                  '''
        return self._run_cmd(cql_cmd)
    
    def create_user(self, props):
        props = self._cql_formater(props)
        cql_cmd = f'''
                    CREATE (p{props})
                    RETURN p
                  '''
        return self._run_cmd(cql_cmd)

    def delete_user(self, props):
        props = self._cql_formater(props)
        cql_cmd = f'''
                    MATCH (p{props})
                    DELETE p
                  '''
        self._run_cmd(cql_cmd)


    


    #def profiles_to_db(pros):

            