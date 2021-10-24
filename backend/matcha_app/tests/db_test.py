import testttest
import sys
import time
import logging #to print in testttest
import inspect
import platform
import neo4j
from neo4j import GraphDatabase as neo4j_db

os = platform.system()
if os == 'Windows':
    sys.path.append('C:/Users/trps/Documents/my_stuff/coding/matcha/backend/matcha_app/')
if os == 'Darwin':
    sys.path.append('/Users/trponess/Documents/matcha/backend/matcha_app/')

import db as db_FILE


class Test:

    #***************************************************************************************
    #  TEST  (no mock for neo4j)
    #  #monolithic test
    #  be careful how you clean up a test env, do not trigger a released db
    #  SETUP for futur tests create users delete them at end 
    #  add 'sig':'for_test_db' property to everything in order to clean up env easily
    # db close is not tested, its guaranteed to suceed, its a simple as pulling out the plug
    # the driver is always avalailable, even if wrong auth or closed, dont test the driver
    #
    # i put elf.print_info inside print functions cause i can leave them in the code without having to add if print_info everywhere 
    #***************************************************************************************

    def __init__(self, uri, userName, pwd, print_info=False):
        self.uri = uri
        self.userName = username
        self.password = pwd
        self.db_inst = None #init in test
        self.sig = f'tmp_test_data_session_{self.timestamp()}' #signature for db elem
        self.print_info = print_info

        self.set_test_data() #all the data the tests are gonna use
        self.tests = self.get_instance_test_methods() #all the tests to launch
        self.error_msgs = dict() #{for_test: msg} to print in conclusion

    def __enter__(self):
        return self

    def __exit__(self):
        if self.db_inst:
            self.clean_env(self.db_inst)
            self.db_inst.close_db()
    
    

    #TEST ENV FNS###############################################################################################################################################

    def set_test_data():
        self.test_users = []
        self.test_users.append({'sig':self.sig, 'name':'crash', 'email':'crash@crapmail.com', 'born':'27/02/1996', 'sex_ori':'female','ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'crash', 'email':'crash_2@crapmail.com' , 'born':'27/02/1996', 'sex_ori':'female', 'ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'crash', 'email':'bad@crapmail.com' , 'born':'27/02/1996', 'sex_ori':'female', 'ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'maria', 'email':'maria@crapmail.com', 'born':'10/04/1994', 'sex_ori':'male','ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'exodia', 'email':'exodia@dumpmail.com', 'born':'01/01/1996', 'sex_ori':'female','ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'iswear', 'email':'iswear@dumpmail.com', 'born':'02/07/1999', 'sex_ori':'male female','ban':'false'})

    def get_instance_test_methods(self):
        #Test.__dict__ does not access self
        all_fns = inspect.getmembers(self, predicate=inspect.ismethod)
        test_fns = [x[1] for x in all_fns if x[0].startswith('test')]
        return dict.fromkeys(test_fns) #all vals None
        
    def conclusion(self):
        
        passed = list(filter(lambda res: res == True, self.tests.values()))
        failed = list(filter(lambda res: res == False, self.tests.values()))
        not_tested = list(filter(lambda res: res is None, self.tests.values()))
        
        print(f'nb_tests:   {len(self.tests)}')
        print(str(' ' * 4) + f'passed:     {len(passed)}')
        print(str(' ' * 4) + f'failed:     {len(failed)}')
        print(str(' ' * 4) + f'not_tested: {len(not_tested)}')

        print()
        print(f'error msgs: {len(self.error_msgs)}')
        i = 0
        for test_name, msg in self.error_msgs.items():
            print(f'TEST ERROR {i}. {test_name}')
            if isinstance(msg, list):
                for i,p in enumerate(msg):
                    print(str(' ' * 4) + f'part {i}')
                    print(str(' ' * 8) + msg)    
            else:
                print(str(' ' * 4) + msg)


    
    def clean_env(self, db_inst):
        #the arg db_inst must seem superfluous cause we have access to self, but it explicit that this test needs a db_inst to work
        cql_clean = f'''
                        MATCH (all) WHERE all.sig='{self.sig}'
                        DELETE all
                    '''
        cql_nb_test_nodes = f'''
                                MATCH (all) WHERE all.sig='{self.sig}'
                                RETURN count(all)
                             '''
        
        print('BEFORE CLEAN')
        n = db_inst._run_cmd(cql_nb_test_nodes)
        print(str(' ' * 4) + f'nb_nodes:{n}' )
        db_inst._run_cmd(cql_clean)
        print('AFTER CLEAN')
        n = db_inst._run_cmd(cql_nb_test_nodes)
        print(str(' ' * 4) + f'nb_nodes:{n}' )


    #UTIL FNS#########################################################################################################################################

    def add_test_tag_to_all_elems(self):
        cql = f'''MATCH (all) 
                  SET all += {self.sig}
                '''
        self.db_inst._run_cmd(cql)
        
    def get_exc_msg(self, extra_info=''):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        #testx uses \r while windows \r
        msg = str(exc_value).replace('\n', '').replace('\r', '')
        msg = msg[0:100]
        err_name = exc_type.__name__
        return f'exception: {err_name} -> {extra_info} : {msg} ...'

    def timestamp(self):
        epoch_now = time.time()
        structtime_now = time.localtime(epoch_now)
        format_now = time.strftime("%Y-%m-%d %H:%M:%S", structtime_now)
        return format_now
        
    def print_obj_res(self, result, override=False):
        
        if not self.print_info and not override:
            return 

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


    def print_log(self, msg, override=False):
        if self.print_info or override:
            #to print in testttest
            logging.basicConfig(stream=sys.stderr)
            log = logging.getLogger("TestDb")
            log.setLevel(logging.DEBUG)
            log.debug(msg)
    
    def print_cql(self, msg, override=False):
        if self.print_info or override:
            print(self.timestamp().center(100, '*'))
            print(f'CQL >>> {msg}'.ljust(50))
            #print('*' * 100)     #can output inside print_obj_res to form a box
    
    def print_msg(self, msg, override=False)
        if self.print_info or override:
            print(msg)

    def run_cmd(cmd):
        print_cql(cmd)
        r = self.db_inst._run_cmd()
        print_obj_res(r)
        return r


    #########################################################################################################################################################

    def run_tests(self):
        fail = False
        for i,test in enumerate(self.tests.keys()):
            self.add_test_tag_to_all_elems() #if any new node, it will give it the self.sig
            print(f'TEST {i}. {test.__name__} '.ljust(100, '-'), end=' ')
            res = test()
            if fail:
                print(f'?'.ljust(20))
            elif res:
                self.tests[test] = True
                print(f'P'.ljust(20))
            else:
                fail = True
                self.tests[test] = False
                print(f'F'.ljust(20))
        self.conclusion()

    #TESTS ############################################################
             



    def test_db_connection(self):
        test_nickname = 'test_db_connection'  #no way to get name of fun in fun
        err_msgs = []

        try:
            with proj.Db(self.uri, self.userName, self.password) as db_inst:
                db_inst._run_cmd('MATCH (n) RETURN n')
                
        except neo4j.exceptions.ServiceUnavailable:
            #normally except ConnectionRefusedError: is raised but is jumpred now i catch this for some reason
            err_msgs.append(self.get_exc_msg("DATABASE NOT ACTIVE"))
        except neo4j.exceptions.AuthError:
            err_msgs.append(self.get_exc_msg("WRONG CREDENTIALS"))
        except Exception:
            err_msgs.append(self.get_exc_msg())
       
        if len(err_msgs) > 0: #failed
            self.error_msgs[test_nickname] = err_msgs
            return False
        else:
            self.db_inst = proj.Db(self.uri, self.userName, self.password)
            self.print_msg(self.db_inst)
            return True 
        
        

    """
    def test_create(self):
        #check for dups
        #only check names
        self.test_print(self.db_inst)
        self.test_print('-----')

        for t in self.test_users:
            self.db_inst.create_user(t)
        for t in self.test_users:
            self.db_inst.create_user(t)
        
        r = self.db_inst._run_cmd(self.cmds('match_props', self.test_users))
        self.assertEquals(len(r), len(self.test_users))
    

    
    #test_create must suceed ot run this test
    def test_ban(self):
        email = 'bad@crapmail.com'
        self.driver.ban_user('bad@crapmail.com', 'true')
        r = self.run_cmd(f'''MATCH(p:Person) WHERE p.name="{email}" AND p.ban="true" RETURN p''')
        self.assertEquals(self.dbres_get(r, 0, 'ban'), 'true')
        self.driver.ban_user('bad@crapmail.com', 'false')
        r = self.run_cmd(f'''MATCH(p:Person) WHERE p.name="{email}" AND p.ban="false" RETURN p ''')
        self.assertEquals(self.dbres_get(r, 0, 'ban'), 'false')
        self.driver.ban_user('bad@crapmail.com', 'false')
        self.driver.ban_user('bad@crapmail.com', 'true')
        r = self.run_cmd(f'''MATCH(p:Person) WHERE p.name="{email}" AND p.ban="true" RETURN p''')
        self.assertEquals(self.dbres_get(r, 0, 'ban'), 'true')


    def test_like(self):
        email = 'crash@crapmail.com'
        email2 = 'maria@crapmail.com'
        
        self.driver.like_user('crash@crapmail.com', 'maria@crapmail.com', 'test')
        r = self.run_cmd(f'''MATCH (p:Person)-[r:LIKES]-(p2:Person) WHERE p.name="{email}" AND p2.name="{email2} RETURN r"''')
        self.assertEqual(len(r), 1)
        r = self.driver.has_relationship('crash@crapmail.com', 'maria@crapmail.com')
        self.assertEqual(r, True)
        r = self.driver.has_relationship('maria@crapmail.com', 'crash@crapmail.com')
        self.assertEqual(r, False)

        self.driver.unlike_user('crash@crapmail.com', 'maria@crapmail.com') 
        r = self.run_cmd(f'''MATCH (p:Person)-[r:LIKES]-(p2:Person) WHERE p.name="{email}" AND p2.name="{email2} RETURN r"''')
        self.assertEqual(len(r), 1)
        r = self.driver.has_relationship('crash@crapmail.com', 'maria@crapmail.com')
        self.assertEqual(r, False)
        r = self.driver.has_relationship('maria@crapmail.com', 'crash@crapmail.com')
        self.assertEqual(r, False)
       
    
    def test_write(self):

        self.driver.write_msg('crash@crapmail.com', 'maria@crapmail.com', 'maria! give me the business', 'test')
        self.driver.write_msg('crash@crapmail.com', 'maria@crapmail.com', 'second thought, give me the good news', 'test')
        self.driver.write_msg('maria@crapmail.com', 'crash@crapmail.com', 'youre officialy 30 years old young and its a beautiful day outside, think about that!', 'test')
        self.driver.write_msg('crash@crapmail.com', 'maria@crapmail.com', 'hmmmm, positive vibes but my animal nature pushes me to crave more', 'test')
        self.driver.write_msg('maria@crapmail.com', 'crash@crapmail.com', 'the ps5 came out and theres free food at burgerking', 'test')
        self.driver.write_msg('crash@crapmail.com', 'maria@crapmail.com', 'sweet precious life, come to me', 'test')
        self.driver.write_msg('exodia@dumpmail.com', 'crash@crapmail.com', 'you greedy basterd', 'test')

        r = self.driver.get_discussion('crash@crapmail.com', 'maria@crapmail.com')
        #print(r)
    
    
        r = self.driver.fetch_all('created_on','-')
        r = self.driver.fetch_all('created_on','+')
    
    
    
    def test_sort_filter():

        all = self.driver.fetch_all() 
        print(len(all))
        all = self.driver.fetch_all('email', '-') 
        print(len(all))
        all = self.driver.fetch_all('born', '-') 
        print(len(all))
        all = self.driver.fetch_all('email', '+', {'name':'crash'}) #filter
        print(len(all))
        #assertequals(len(all) == 3)
        all = self.driver.fetch_all('email', '+', {'name':'crash','ban':'true'}) #filter
        print(len(all))
        #assertequals(len(all) == 2)
        all = self.driver.fetch_all('email', '+', {'name':'crash','ban':'false'}) #filter
        print(len(all))
        #assertequals(len(all) == 1)
        all = self.driver.fetch_all('email', '+', {'name':'crash','born':'27/02/1996'}) #filter
        print(len(all))
        #assertequals(len(all) == 3)
        all = self.driver.fetch_all('email', '+', {'slddls':'07ii'}) #non existed filter
        print(len(all))
    """

    
    
        

if __name__ == '__main__':

    #testtest uses argv, mack sure to remove your own, use -- on yours
    '''
    if len(sys.argv) > 1:
        TestDb.URI = sys.argv.pop()
        TestDb.PASSWORD = sys.argv.pop()
        TestDb.PASSWORD = sys.argv.pop()
    '''

    with Test("bolt://localhost:7687", "neo4j", "0000") as test_session:
        test_session.run_tests()