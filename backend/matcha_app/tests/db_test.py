# Standard library imports
import sys
import time
import logging 
import inspect
import platform
import os
from io import StringIO

# Third party imports
import neo4j
from neo4j import GraphDatabase as neo4j_db

#inner project
f = os.path.dirname(__file__)
x = os.path.join(f, '..')
sys.path.append(x)
import db


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
        #print_info it's own ouput, cql, tested_module_output, to stdout/file
        self.uri = uri
        self.userName = userName
        self.password = pwd
        self.db_inst = None #init in test
        self.sig = f'tmp_test_data_session_{self.timestamp()}' #signature for db elem
        self.print_info = print_info

        self.set_test_data() #all the data the tests are gonna use
        self.tests = self.get_instance_test_methods() #all the tests to launch
        self.set_output_files()
        self.error_msgs = dict() #{for_test: msg} to print in conclusion

        self.output_buffer = ''

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db_inst._driver:
            self.clean_env(self.db_inst)
            self.db_inst.close_db()
    
    

    #TEST ENV FNS###############################################################################################################################################

    def set_test_data(self):
        self.test_users = []
        self.test_users.append({'sig':self.sig, 'name':'crash', 'email':'crash@crapmail.com', 'birthdate':'27/02/1996', 'sex_ori':'female','ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'crash', 'email':'crash_2@crapmail.com' , 'birthdate':'27/02/1996', 'sex_ori':'female', 'ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'crash', 'email':'bad@crapmail.com' , 'birthdate':'27/02/1996', 'sex_ori':'female', 'ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'maria', 'email':'maria@crapmail.com', 'birthdate':'10/04/1994', 'sex_ori':'male','ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'exodia', 'email':'exodia@dumpmail.com', 'birthdate':'01/01/1996', 'sex_ori':'female','ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'iswear', 'email':'iswear@dumpmail.com', 'birthdate':'02/07/1999', 'sex_ori':'male female','ban':'false'})
    
    
    def set_output_files(self):
        self.root = os.path.dirname(__file__)
        self.cql_output = os.path.join(self.root, 'test_outputs/cql_cmds.txt')
        self.tested_module_output = os.path.join(self.root, 'test_outputs/tested_module_output.txt')

        self.empty_file(self.cql_output)
        self.empty_file(self.tested_module_output)

    def get_instance_test_methods(self):
        #Test.__dict__ does not access self
        #test_N_name makes them sorted alpha, so extra sorted needed
        all_fns = inspect.getmembers(self, predicate=inspect.ismethod)
        test_fns = [x[1] for x in all_fns if x[0].startswith('test')]
        return dict.fromkeys(test_fns) #all vals None
        
    def conclusion(self):
        
        passed = list(filter(lambda res: res == True, self.tests.values()))
        failed = list(filter(lambda res: res == False, self.tests.values()))
        not_tested = list(filter(lambda res: res is None, self.tests.values()))

        #
        print(f'nb_tests:   {len(self.tests)}')
        print(str(' ' * 4) + f'passed:     {len(passed)}')
        print(str(' ' * 4) + f'failed:     {len(failed)}')
        print(str(' ' * 4) + f'not_tested: {len(not_tested)}')

        #print_info

        #error_msgs
        print()
        print(f'error msgs: {len(self.error_msgs)}')
        i = 0
        for test_name, msg in self.error_msgs.items():
            print(str(' ' * 4) + f'TEST ERROR {i}. {test_name}')
            if isinstance(msg, list):
                for i,p in enumerate(msg):
                    print(str(' ' * 8) + f'>exception {i}<')
                    print(str(' ' * 12) + p)
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

    def capture_stdout(self):
        sys.stdout = StringIO()
        self.output_buffer += sys.stdout.getvalue()
        '''
        if 'belongs to model'
            keep in buffer 
        else 
            take out of buffer or dont put in and direct print 
            print()
        '''

    #UTIL FNS#########################################################################################################################################

    def add_testsig_to_node(self, r):
        cql = f'''MATCH (p)
                  WHERE p.email = "{r['email']}"
                  SET p.sig = "{self.sig}"
                '''
        self.db_inst._run_cmd(cql)

    def timestamp(self):
        epoch_now = time.time()
        structtime_now = time.localtime(epoch_now)
        format_now = time.strftime("%Y-%m-%d %H:%M:%S", structtime_now)
        return format_now
        
    def print_obj_res(self, result, override=False):
        
        if self.print_info == False and override == False:
            return 

        self.write_file('db res'.center(100, '-'))

        if isinstance(result,str): #relationships are strings
                        self.write_file(result)
        #neo4j.Result.data -> lst of dicts 
        elif isinstance(result,list):
            for lst_elem in result:
                
                for k,v in lst_elem.items():
                    self.write_file(f'cql return var:{k} -> {v}')
                    

                    
        else:
            #neo4j.Result gets moved out the iter causing res to be empty
            #i didnt find a way to do a copy of this obj
            for record in result:
                self.write_file(record.keys())
                for cql_return_tag in record.keys():
                    
                    self.write_file('cql return var: ', cql_return_tag)
                    node = record[cql_return_tag]
                    #self.write_file(record.keys())
                    #self.write_file(type(record['n']))
                    if isinstance(node,str): #relationships are strings
                        self.write_file(node)
                    else:
                        self.write_file(f'{node.labels} {node.items()}')
        self.write_file('end'.center(100, '-'))
        self.write_file('*' * 100)  #to stock inside log text box 
    
    def empty_file(self, file):
        with open(file, 'w') as f:
            pass

    def write_file(self, line, file=''):
        #clear everytime
        if file == '':
            file = self.cql_output
        with open(file, 'a') as f:
            line += '\n'
            f.writelines([line])

    def print_log(self, msg, override=False):
        if self.print_info or override:
            #to print in testttest
            logging.basicConfig(stream=sys.stderr)
            log = logging.getLogger("TestDb")
            log.setLevel(logging.DEBUG)
            log.debug(msg)
    
    def print_cql(self, msg, override=False):
        if self.print_info or override:
            self.write_file(self.timestamp().center(100, '*'), self.cql_output)
            self.write_file(f'CQL >>> {msg}'.ljust(50), self.cql_output)
            #print('*' * 100)     #can output inside print_obj_res to form a box
    
    def print_msg(self, msg, override=False):
        if self.print_info or override:
            self.write_file(msg, self.tested_module_output)

    def run_cmd(self, cmd, return_type=''):
        self.print_cql(cmd)
        r = self.db_inst._run_cmd(cmd, return_type)
        if 'create' in cmd.lower():
            self.add_testsig_to_node(r[0])
        self.print_obj_res(r)
        return r


    #########################################################################################################################################################

    def run_tests(self):
        fail = False
        for i,test in enumerate(self.tests.keys()):
            print(f'TEST {i}. {test.__name__} '.ljust(100, '-'), end=' ')
            if not fail:
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

    def test_1_db_connection(self):
        test_nickname = 'test_db_connection'  #no way to get name of fun in fun

        self.db_inst = db.Db(self.uri, self.userName, self.password)

        if len(self.db_inst.err_msgs) > 0: #failed
            self.error_msgs[test_nickname] = self.db_inst.err_msgs
            return False
        return True 

    
    def test_2_create(self):
        #check for dups
        #only check names
        
        for t in self.test_users:
            cql = self.db_inst.cql_create_user(t)
            self.run_cmd(cql)
        for t in self.test_users:
            cql = self.db_inst.cql_create_user(t)
            self.run_cmd(cql)
        
        #r = self.db_inst._run_cmd(f'match (p) where p.email="" return p')
        #return len(r) == len(self.test_users)
        return False
    
    

    """
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
        all = self.driver.fetch_all('birthdate', '-') 
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
        all = self.driver.fetch_all('email', '+', {'name':'crash','birthdate':'27/02/1996'}) #filter
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

    

    #['cql': 'file', 'tested_module': 'file', 'exceptions']
    with Test("bolt://localhost:7687", "neo4j", "0000", True) as test_session:
        test_session.run_tests()


'''
exc = 200
import sys

import traceback
import sys

def get_exception():
    
    exc_type, exc_value, exc_traceback = sys.exc_info()
    
    filename = exc_traceback.tb_frame.f_code.co_filename
    lineno   = exc_traceback.tb_lineno
    name     = exc_traceback.tb_frame.f_code.co_name
    type_     = exc_type.__name__
    message  = str(exc_value) # or see traceback._some_str()

    #
    trace_back = traceback.extract_tb(exc_traceback)
    # Format stacktrace
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append(trace)
    st = '\n'.join(str(x) for x in stack_trace)
    #

    deco_top = 'MATCHA ERROR'.center(50, '#')
    deco_bottom = ''.center(50, '#')
    err_msg = f"{type_} > {filename} [l{lineno}] in {name}  :: {st}"

    return f'\n{deco_top}\n{err_msg}\n{deco_bottom}\n'

class X:
    
    def __init__(self):
        self.data = self.try_()
        
    def try_(self):
        try:
            return 3/0 
        except Exception:
            try:
                raise ValueError
            except Exception:
                print(get_exception())
            print(get_exception())
            print(get_exception())
            
        
    def __enter__(self):
        return self
    def __exit__(self,a,b,c):
        print('exit called')



with X() as i:
    print(i.data)
'''