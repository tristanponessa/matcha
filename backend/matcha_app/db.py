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
tags = ('drawing','coding','politics','chess','sports','workout','sleeping','skydiving','movies','reading','creating','cooking','dancing','driving','travel')


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
        try:
            self.__driver = neo4j_db.driver(uri, auth=(userName, password))
            print('starting db')
        except Exception:
            print('ERROR: Could not connect to the Neo4j Database. See console for details.')
            sys.exit(0)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close_db()
        if exc_type:
            print(f'__exit__ says: exc_type: {exc_type}')
            print(f'__exit__ says: exc_value: {exc_value}')
            print(f'__exit__ says: exc_traceback: {exc_traceback}')

    def get_driver(self):
        #for tests only
        return self.__driver

    def close_db(self):
        self.__driver.close()
        print('closing db')
    
    def __run_cmd(self, cmd):
        with self.__driver.session() as session:
            self.__log_msg(cmd)
            result_obj =  session.run(cmd)
            result = result_obj.data() #lst of dcts
            self.__print_obj_res(result) #cant return data empty
            return result

    def __timestamp(self):
        epoch_now = time.time()
        structtime_now = time.localtime(epoch_now)
        format_now = time.strftime("%Y-%m-%d %H:%M:%S", structtime_now)
        return format_now
    
    def __cql_formater(self, d: dict):
        #1.converts str to cql types for correct sorting/filtering
        #neo4j proposes a format string with $var instead of {}
        #2.{'name':'val'} converts to -> {name:'val'}

        for v in d.values():
            if '/' in v:
                v = self.__cql_type('date', v)

        dstr = json.dumps(d) #json transforms ' to "
        for k in d.keys():
            dstr = dstr.replace(f'"{k}"', k)
        return dstr
    
    def __cql_type(self, type, data):
        if type == 'timestamp':
            return f"date('{data}')"
        if type == 'date':
            #must be /day/month/year-> year-month-day
            v = data
            v = v.split('/')
            v.reverse()
            v = "-".join(v)
            return f"date('{v}')"


    def run_cmd(self, cql_cmd):
        return self.__run_cmd(cql_cmd)
    
    def db_result_format(self, res):
        #session.runs returns a list of dicts [{'cql return name': {'key1','val1'}, ...]
        #we trasform into      list of dicts  [{'key1','val1'}]
        print('->', res)
        r = [list(dct.values())[0] for dct in res]
        print('+>', r)
        return r if len(r) > 0 else None


    
    def has_relationship(self, email1, email2):
        #left to right
        cql_cmd = '''
                    MATCH (p:Person) WHERE p.email="{}"
                    MATCH (to:Person) WHERE to.email="{}"
                    MATCH (p)-[r:LIKES]->(to)
                    RETURN r
                  '''.format(email1, email2)
        r = self.__run_cmd(cql_cmd) 
        return len(r) > 0

    def fetch_all(self, prop='name', order='+', filter_args=None):

        #can sort and filter
        filter = []
        filter_str = ''
        if filter_args:
            for prop,val in filter_args.items():
                filter.append(f'all.{prop}="{val}"')
            filter_str = " AND ".join(filter)
            filter_str = f'WHERE {filter_str}'

        order = 'ASC' if order == '+' else 'DESC'
        cql_cmd = '''
                    MATCH (all)
                    {filter_str_}
                    RETURN all
                    ORDER BY all.{prop_} {order_}
                  '''.format(filter_str_=filter_str, prop_=prop, order_=order)
        
        return self.__run_cmd(cql_cmd)

    def user_exists(self, email):
        cql_cmd = '''
                    MATCH (p:Person)
                    WHERE p.email="{}"
                    RETURN p
                  '''.format(email)
        res = self.__run_cmd(cql_cmd)
        return res

    
    def ban_user(self, email, state):
        cql_cmd = '''
                    MATCH (p:Person) WHERE p.email="{}"
                    SET p.ban="{}"
                    RETURN p
                  '''.format(email, state)
        return self.__run_cmd(cql_cmd)
    

    def write_msg(self, from_email, to_email, msg, testid=''):

        if testid == 'test':
            testid = '''
                        SET new_msg.sig="for_test_db"
                        SET r1.sig="for_test_db"
                        SET r2.sig="for_test_db"
            '''

        cql_date = self.__cql_type('timestamp', self.__timestamp())
        cql_cmd = '''
                    MATCH(src:Person) WHERE src.email="{}"
                    MATCH(dst:Person) WHERE dst.email="{}"
                    CREATE (src)-[r1:WROTE]->(new_msg:Msg)-[r2:DESTINED_TO]->(dst)
                    SET new_msg.input = "{}" 
                    SET new_msg.created_on="{}"
                    {}
                    RETURN src,type(r1),new_msg,type(r2),dst
                  '''.format(from_email, to_email, msg, cql_date, testid)
        return self.__run_cmd(cql_cmd)
    
    def get_discussion(self, from_email, to_email):
        cql_cmd = '''
                    MATCH(src:Person) WHERE src.email="{}"
                    MATCH(dst:Person) WHERE dst.email="{}"
                    MATCH (src)-[:WROTE]->(msg:Msg)-[:DESTINED_TO]->(dst)
                    RETURN src,msg,dst
                  '''.format(from_email, to_email)
        return self.__run_cmd(cql_cmd)

    
    def create_user(self, data: dict):
        #merge prevents duplicate creation
        cql_dct_str = self.__cql_formater(data)
        cql_cmd = '''
                    MERGE (new_user:Person{})
                    RETURN new_user
                  '''.format(cql_dct_str)
        return self.__run_cmd(cql_cmd)
    
    def like_user(self, from_email, to_email, testid=''):
        #MERGE (src)-[r:LIKES{date:"{}"}]->(dst)   driver causing problem about merge the security to prevent duplication 
        testid = "SET r.sig='for_test_db'" if testid == 'test' else ''
        cql_date = self.__cql_type('timestamp', self.__timestamp())
        cql_cmd = '''
                    MATCH (src:Person) WHERE src.email="{}"
                    MATCH (dst:Person) WHERE dst.email="{}"
                    MERGE (src)-[r:LIKES]->(dst)
                    SET r.date="{}"
                    {}
                  '''.format(from_email, to_email, cql_date, testid)
        self.__run_cmd(cql_cmd)
    
    def unlike_user(self, from_email, to_email):
        cql_cmd = '''
                    MATCH (src:Person) WHERE src.email="{}"
                    MATCH (dst:Person) WHERE dst.email="{}"
                    MATCH (src)-[r:LIKES]->(dst)
                    DELETE r
                  '''.format(from_email, to_email)
        self.__run_cmd(cql_cmd)
    
    def hobbies_tag(self, email, tag):
        cql_cmd = '''
                    MATCH (src:Person) WHERE src.email="{}"
                    MATCH (tag:Tag) WHERE tag.name="{}"
                    MERGE (src)-[r:HAS_HOBBY{date:"{}"}]->(tag)
                    RETURN *
                  '''.format(email, tag, self.__timestamp())
        return self.__run_cmd(cql_cmd)
    
    def unhobbies_tag(self, email, tag):
        cql_cmd = '''
                    MATCH (src:Person) WHERE src.email="{}"
                    MATCH (tag:Tag) WHERE tag.name="{}"
                    MATCH (src)-[r:HAS_HOBBY]->(tag)
                    DELETE r
                  '''.format(email, tag)
        self.__run_cmd(cql_cmd)
    
    def delete_user(self, email):
        cql_cmd = '''
                    MATCH (src:Person) WHERE src.email="{}"
                    DELETE src
                  '''.format(email)
        self.__run_cmd(cql_cmd)

    def __log_msg(self, msg):
        print(self.__timestamp().center(100, '*'))
        print(f'CQL >>> {msg}'.ljust(50))
        #print('*' * 100)

    def __print_obj_res(self, result):
        
        print('db res'.center(100, '-'))

        if isinstance(result,str): #relationships are strings
                        print(result)
        #neo4j.Result.data -> lst of dicts 
        elif isinstance(result,list):
            for lst_elem in result:
                
                for k,v in lst_elem.items():
                    print(f'cql return var:{k}', end=' -> ')
                    print(v)
                    
        else:
            #neo4j.Result gets moved out the iter causing res to be empty
            #i didnt find a way to do a copy of this obj
            for record in result:
                print(record.keys())
                for cql_return_tag in record.keys():
                    
                    print('cql return var: ', cql_return_tag)
                    node = record[cql_return_tag]
                    #print(record.keys())
                    #print(type(record['n']))
                    if isinstance(node,str): #relationships are strings
                        print(node)
                    else:
                        print(node.labels, end=' ')
                        print(node.items())
        print('end'.center(100, '-'))
        print('*' * 100)  #to stock inside log text box 





if __name__ == '__main__':
    
    #***************************************************************************************
    #  TEST  mock OR load test_db
    #  be careful how you clean up a test env, do not trigger an active db
    #  SETUP for futur tests create users delete them at end 
    #  add 'sig':'for_test_db' property to everything in order to clean up env easily
    #  prevent using fns from your app to turn on db or delete, make sure to work fns jsut for test
    #***************************************************************************************
    
        test_users = []
        test_users.append({'sig':'for_test_db', 'name':'crash', 'email':'crash@crapmail.com', 'born':'27/02/1996', 'sex_ori':'female','ban':'false'})
        test_users.append({'sig':'for_test_db', 'name':'crash', 'email':'crash_2@crapmail.com' , 'born':'27/02/1996', 'sex_ori':'female', 'ban':'false'})
        test_users.append({'sig':'for_test_db', 'name':'crash', 'email':'bad@crapmail.com' , 'born':'27/02/1996', 'sex_ori':'female', 'ban':'true'})
        test_users.append({'sig':'for_test_db', 'name':'maria', 'email':'maria@crapmail.com', 'born':'10/04/1994', 'sex_ori':'male','ban':'false'})
        test_users.append({'sig':'for_test_db', 'name':'exodia', 'email':'exodia@dumpmail.com', 'born':'01/01/1996', 'sex_ori':'female','ban':'false'})
        test_users.append({'sig':'for_test_db', 'name':'iswear', 'email':'iswear@dumpmail.com', 'born':'02/07/1999', 'sex_ori':'male female','ban':'false'})

        with Db("bolt://localhost:7687", "neo4j", "0000") as db_inst:
        #db_inst.fetch_all()

            def print_obj_res(self, result):        
                print('db res'.center(100, '-'))

                if isinstance(result,str): #relationships are strings
                                print(result)
                #neo4j.Result.data -> lst of dicts 
                elif isinstance(result,list):
                    for lst_elem in result:
                        
                        for k,v in lst_elem.items():
                            print(f'cql return var:{k}', end=' -> ')
                            print(v)
                            
                else:
                    #neo4j.Result gets moved out the iter causing res to be empty
                    #i didnt find a way to do a copy of this obj
                    for record in result:
                        print(record.keys())
                        for cql_return_tag in record.keys():
                            
                            print('cql return var: ', cql_return_tag)
                            node = record[cql_return_tag]
                            #print(record.keys())
                            #print(type(record['n']))
                            if isinstance(node,str): #relationships are strings
                                print(node)
                            else:
                                print(node.labels, end=' ')
                                print(node.items())
                print('end'.center(100, '-'))
                print('*' * 100)  #to stock inside log text box
        
            def clean_test_data(db_inst):
                #driver does not work taken outside class
                print('cleaning test env :')

                def count_nb_elems():
                    cql = '''
                            MATCH (all) WHERE all.sig='for_test_db'
                            RETURN all
                    '''

                    cql2 = '''                       
                            MATCH ()-[all_r]-() WHERE all_r.sig='for_test_db'
                            RETURN all_r
                    '''

                    with db_inst.get_driver().session() as session:
                        r = session.run(cql)
                        r2 = session.run(cql2)
                        print('nb_relations:>', len(r.data()))
                        print('nb_nodes:>', len(r2.data()))

                print('before clean:')
                count_nb_elems()

                cql = '''
                        MATCH (all) WHERE all.sig='for_test_db'
                        MATCH ()-[all_r]-() WHERE all_r.sig='for_test_db'                        
                        DELETE all_r
                        DELETE all
                '''
                
                with db_inst.get_driver().session() as session:
                    session.run(cql)

                print('after clean:')
                count_nb_elems()



            try:

                #test0 for futur tests create users delete them at end 
                for t in test_users:
                    db_inst.create_user(t)
                
                '''
                #test anti duplicate create 
                for t in test_users:
                    db_inst.create_user(t)
                for t in test_users:
                    db_inst.create_user(t)
                all = db_inst.fetch_all() 
                print(len(all))
                #assertequals(len(test_users) == len(all))
                '''
                
                


                '''
                #test1
                print(db_inst.user_exists('crash@crapmail.com'))

                #test2 create ban check_if_banned delte search
                db_inst.create_user({'name':'Bad', 'email':'bad@crapmail.com'})
                print(db_inst.user_exists('bad@crapmail.com'))
                db_inst.ban_user('bad@crapmail.com', 'true')
                print(db_inst.user_exists('bad@crapmail.com'))
                db_inst.delete_user('bad@crapmail.com')
                print(db_inst.user_exists('bad@crapmail.com'))

                #test3 
                user_exists1 = db_inst.user_exists('bad@crapmail.com')
                new_user = db_inst.create_user({'name':'Bad', 'email':'bad@crapmail.com'})
                db_inst.ban_user('bad@crapmail.com', True)
                db_inst.ban_user('bad@crapmail.com', 'true')
                db_inst.ban_user('bad@crapmail.com', False)
                db_inst.ban_user('bad@crapmail.com', 'false')
                user_exists2 = db_inst.user_exists('bad@crapmail.com')
                print('user exists? : ', user_exists1)
                print('create user ? : ', new_user)
                print('user exists? : ', user_exists2)

            s
                '''

                #test4 like 
                '''
                db_inst.like_user('crash@crapmail.com', 'maria@crapmail.com', 'test')
                r1 = db_inst.has_relationship('crash@crapmail.com', 'maria@crapmail.com')
                r2 = db_inst.has_relationship('maria@crapmail.com', 'crash@crapmail.com')
                print('a relationship? crash maria ', r1)
                print('a relationship? maria crash', r2)
                db_inst.unlike_user('crash@crapmail.com', 'maria@crapmail.com') 
                r1 = db_inst.has_relationship('crash@crapmail.com', 'maria@crapmail.com')
                r2 = db_inst.has_relationship('maria@crapmail.com', 'crash@crapmail.com')
                print('a relationship? crash maria', r1)
                print('a relationship? maria crash', r2)
                '''
                


                #test5 sort filter
                
                '''
                all = db_inst.fetch_all() 
                print(len(all))
                all = db_inst.fetch_all('email', '-') 
                print(len(all))
                all = db_inst.fetch_all('born', '-') 
                print(len(all))
                all = db_inst.fetch_all('email', '+', {'name':'crash'}) #filter
                print(len(all))
                #assertequals(len(all) == 3)
                all = db_inst.fetch_all('email', '+', {'name':'crash','ban':'true'}) #filter
                print(len(all))
                #assertequals(len(all) == 2)
                all = db_inst.fetch_all('email', '+', {'name':'crash','ban':'false'}) #filter
                print(len(all))
                #assertequals(len(all) == 1)
                all = db_inst.fetch_all('email', '+', {'name':'crash','born':'27/02/1996'}) #filter
                print(len(all))
                #assertequals(len(all) == 3)
                all = db_inst.fetch_all('email', '+', {'slddls':'07ii'}) #non existed filter
                print(len(all))
                '''

                #test6 write msg 
                
                '''
                db_inst.write_msg('crash@crapmail.com', 'maria@crapmail.com', 'maria! give me the business', 'test')
                db_inst.write_msg('crash@crapmail.com', 'maria@crapmail.com', 'second thought, give me the good news', 'test')
                db_inst.write_msg('maria@crapmail.com', 'crash@crapmail.com', 'youre officialy 30 years old young and its a beautiful day outside, think about that!', 'test')
                db_inst.write_msg('crash@crapmail.com', 'maria@crapmail.com', 'hmmmm, positive vibes but my animal nature pushes me to crave more', 'test')
                db_inst.write_msg('maria@crapmail.com', 'crash@crapmail.com', 'the ps5 came out and theres free food at burgerking', 'test')
                db_inst.write_msg('crash@crapmail.com', 'maria@crapmail.com', 'sweet precious life, come to me', 'test')
                db_inst.write_msg('exodia@dumpmail.com', 'crash@crapmail.com', 'you greedy basterd', 'test')

                r = db_inst.get_discussion('crash@crapmail.com', 'maria@crapmail.com')
                #print(r)
            
                r = db_inst.fetch_all('created_on','-')
                r = db_inst.fetch_all('created_on','+')
                '''
                
                

                

            finally:
                #clean up test env
                #before deleting users destroy any relations  theyre are done in the tests
                
                #for t in test_users:
                #    db_inst.delete_user(t['email'])

                clean_test_data(db_inst)


