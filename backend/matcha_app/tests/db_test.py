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

        sys.stdout = StringIO() #all output is stocked in this object

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db_inst._driver:
            self.clean_env(self.db_inst)
            self.db_inst.close_db()
        self.tested_module_output_save()

    #TEST ENV FNS###############################################################################################################################################

    def set_test_data(self):
        self.test_users = []
        self.test_users.append({ 'name':'crash', 'email':'crash@crapmail.com', 'birthdate':'27/02/1996', 'sex_ori':'female','ban':'false'})
        self.test_users.append({ 'name':'crash', 'email':'crash_2@crapmail.com' , 'birthdate':'27/02/1996', 'sex_ori':'female', 'ban':'false'})
        self.test_users.append({ 'name':'crash', 'email':'bad@crapmail.com' , 'birthdate':'27/02/1996', 'sex_ori':'female', 'ban':'false'})
        self.test_users.append({ 'name':'maria', 'email':'maria@crapmail.com', 'birthdate':'10/04/1994', 'sex_ori':'male','ban':'false'})
        self.test_users.append({ 'name':'exodia', 'email':'exodia@dumpmail.com', 'birthdate':'01/01/1996', 'sex_ori':'female','ban':'false'})
        self.test_users.append({ 'name':'iswear', 'email':'iswear@dumpmail.com', 'birthdate':'02/07/1999', 'sex_ori':'male female','ban':'false'})
    
    
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
        test_fns = [x[1] for x in all_fns if x[0].startswith('test_')]
        return dict.fromkeys(test_fns) #all vals None
        
    def conclusion(self):
        
        passed = list(filter(lambda res: res == True, self.tests.values()))
        failed = list(filter(lambda res: res == False, self.tests.values()))
        not_tested = list(filter(lambda res: res is None, self.tests.values()))

        #
        self.print_(f'nb_tests:   {len(self.tests)}')
        self.print_(str(' ' * 4) + f'passed:     {len(passed)}')
        self.print_(str(' ' * 4) + f'failed:     {len(failed)}')
        self.print_(str(' ' * 4) + f'not_tested: {len(not_tested)}')

        #print_info

        #error_msgs
        self.print_()
        self.print_(f'error msgs: {len(self.error_msgs)}')
        i = 0
        for test_name, msg in self.error_msgs.items():
            self.print_(str(' ' * 4) + f'TEST ERROR {i}. {test_name}')
            if isinstance(msg, list):
                for i,p in enumerate(msg):
                    self.print_(str(' ' * 8) + f'>exception {i}<')
                    self.print_(str(' ' * 12) + p)
            else:
                self.print_(str(' ' * 8) + msg)
        self.print_()


    
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
        
        self.print_('BEFORE CLEAN')
        n = self.run_cmd(cql_nb_test_nodes)
        self.print_(str(' ' * 4) + f'nb_nodes:{n}' )
        self.run_cmd(cql_clean)
        self.print_('AFTER CLEAN')
        n = self.run_cmd(cql_nb_test_nodes)
        self.print_(str(' ' * 4) + f'nb_nodes:{n}' )

    def print_(self, *args, **kwargs):
        #stdout goes into StringIO
        print(*args, **kwargs, file=sys.__stdout__)
    
    def tested_module_output_save(self):
        buffer = sys.stdout.getvalue()
        self.write_file(buffer, self.tested_module_output)

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

        if isinstance(result,list):
            for i,lst_elem in enumerate(result):
                self.write_file(f'lst elem {i}')
                #i tried with 'items' in dir(lst_elem) but it inherits so it dont show in this dir, also isinstance( , dict) obj it has items but not dict items() even though their identical
                try: 
                    for k,v in lst_elem.items():
                        self.write_file(str(' ' * 4) + f'{k} -> {v}')
                except AttributeError:
                    self.write_file(str(' ' * 4) + f'{lst_elem}')
        else: #like for cql fn count()
            self.write_file(result)
                    
                
                    

        '''       
        #neo4j.Result.data -> lst of dicts 
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
        '''

        self.write_file('end'.center(100, '-'))
        self.write_file('*' * 100)  #to stock inside log text box 

    
    def empty_file(self, file):
        with open(file, 'w') as f:
            pass

    def write_file(self, lines, file=''):
        #clear everytime
        if isinstance(lines, str):
            lines = [lines]
        if file == '': #cant put self in arg
            file = self.cql_output 
        with open(file, 'a') as f:
            lines += '\n'
            f.writelines(lines)
    
    '''
    def print_debug(self, msg, override=False):
        if self.print_info or override:
            #to print in testttest
            logging.basicConfig(stream=sys.stdout)
            log = logging.getLogger("TestDb")
            log.setLevel(logging.DEBUG)
            log.debug(msg)
    '''

    def print_cql(self, msg, override=False):
        if self.print_info or override:
            self.write_file(self.timestamp().center(100, '*'), self.cql_output)
            self.write_file(f'CQL >>> {msg}'.ljust(50), self.cql_output)
            #self.print_('*' * 100)     #can output inside print_obj_res to form a box
    
    '''
    def print_msg(self, msg, file, override=False):
        if self.print_info or override:
            self.write_file(msg, file)
    '''

    def run_cmd(self, cmd, return_type=''):
        self.print_cql(cmd)
        r = self.db_inst._run_cmd(cmd, return_type)
        if 'create' in cmd.lower() or 'merge' in cmd.lower():
            self.add_testsig_to_node(r[0])
        self.print_obj_res(r)
        return r
    
    def cmds(self, which, lst):
        if which == 'match_props':
            j = []
            for t in lst:
                j.append(f'''p.email="{t['email']}"''')
            j = ' OR '.join(j)
            x = f'''
                    MATCH (p)
                    WHERE {j}
                    RETURN p
            '''
            return x


    #########################################################################################################################################################

    def run_tests(self):
        fail = False
        for i,test in enumerate(self.tests.keys()):
            self.print_(f'TEST {i}. {test.__name__} '.ljust(100, '-'), end=' ')
            if not fail:
                res = test()
            if fail:
                self.print_(f'?'.ljust(20))
            elif res:
                self.tests[test] = True
                self.print_(f'P'.ljust(20))
            else:
                fail = True
                self.tests[test] = False
                self.print_(f'F'.ljust(20))
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
        test_nickname = 'create'
        
        for t in self.test_users:
            cql = self.db_inst.cql_create_user(t)
            self.run_cmd(cql)
        for t in self.test_users:
            cql = self.db_inst.cql_create_user(t)
            self.run_cmd(cql)
        
        r = self.run_cmd(self.cmds('match_props', self.test_users))
        if len(r) != len(self.test_users):
            self.error_msgs[test_nickname] = f'to create {len(self.test_users)} created {len(r)}'
        else:
            return True
    
    

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
        #self.print_(r)
    
    
        r = self.driver.fetch_all('created_on','-')
        r = self.driver.fetch_all('created_on','+')
    
    
    
    def test_sort_filter():

        all = self.driver.fetch_all() 
        self.print_(len(all))
        all = self.driver.fetch_all('email', '-') 
        self.print_(len(all))
        all = self.driver.fetch_all('birthdate', '-') 
        self.print_(len(all))
        all = self.driver.fetch_all('email', '+', {'name':'crash'}) #filter
        self.print_(len(all))
        #assertequals(len(all) == 3)
        all = self.driver.fetch_all('email', '+', {'name':'crash','ban':'true'}) #filter
        self.print_(len(all))
        #assertequals(len(all) == 2)
        all = self.driver.fetch_all('email', '+', {'name':'crash','ban':'false'}) #filter
        self.print_(len(all))
        #assertequals(len(all) == 1)
        all = self.driver.fetch_all('email', '+', {'name':'crash','birthdate':'27/02/1996'}) #filter
        self.print_(len(all))
        #assertequals(len(all) == 3)
        all = self.driver.fetch_all('email', '+', {'slddls':'07ii'}) #non existed filter
        self.print_(len(all))
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


