import unittest
import sys
import time
from neo4j import GraphDatabase as neo4j_db



#def print_cql:
#def print_res:




class TestDb(unittest.TestCase):

    #***************************************************************************************
    #  TEST  (no mock for neo4j)
    #  be careful how you clean up a test env, do not trigger an active db
    #  SETUP for futur tests create users delete them at end 
    #  add 'sig':'for_test_db' property to everything in order to clean up env easily
    #  prevent using fns from your app to turn on db or delete, make sure to work fns jsut for test
    #***************************************************************************************

    def setUp(self):
        #! very bad news: neo4j lets you connect despite the auth being wrong, there's no auth checking and its not mentioned in the doc

        self.uri = "bolt://localhost:7687"
        self.userName = 'test'
        self.password = '0000'
        self.sig = 'for_test_db' #signature for db elem

        try:
            self.driver = neo4j_db.driver(self.uri, auth=(self.userName, self.password))
        except Exception as e:
            assert False, f'UNITEST SETUP: {e}'
        
        self.cql_get_test_nodes = f'''MATCH (all) WHERE all.sig='{self.sig}'
                                         RETURN count(all)
                                      '''
        self.cql_get_test_relations = f'''MATCH ()-[all_r]-() WHERE all_r.sig='{self.sig}'
                                      RETURN count(all_r) '''

        self.test_users = []
        self.test_users.append({'sig':self.sig, 'name':'crash', 'email':'crash@crapmail.com', 'born':'27/02/1996', 'sex_ori':'female','ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'crash', 'email':'crash_2@crapmail.com' , 'born':'27/02/1996', 'sex_ori':'female', 'ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'crash', 'email':'bad@crapmail.com' , 'born':'27/02/1996', 'sex_ori':'female', 'ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'maria', 'email':'maria@crapmail.com', 'born':'10/04/1994', 'sex_ori':'male','ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'exodia', 'email':'exodia@dumpmail.com', 'born':'01/01/1996', 'sex_ori':'female','ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'iswear', 'email':'iswear@dumpmail.com', 'born':'02/07/1999', 'sex_ori':'male female','ban':'false'})

        


    def timestamp(self):
        epoch_now = time.time()
        structtime_now = time.localtime(epoch_now)
        format_now = time.strftime("%Y-%m-%d %H:%M:%S", structtime_now)
        return format_now

    def log_msg(self, msg):
        print(self.__timestamp().center(100, '*'))
        print(f'CQL >>> {msg}'.ljust(50))
        #print('*' * 100)
    
    def db_result_format(self, res):
        #session.runs returns a list of dicts [{'cql return name': {'key1','val1'}, ...]
        #we trasform into      list of dicts  [{'key1','val1'}]
        r = [list(dct.values())[0] for dct in res]
        return r if len(r) > 0 else None
    
    def dbres_get(self, r, index, prop=None):
        dct = r[index] if index < len(r) else None
        return dct.get(prop) if prop else dct
        
        

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

    def cmds(self, which, lst):
        if which == 'match_props':
            j = []
            for t in lst:
                j.append(f'p.name="{t.name}"')
            j = ' AND '.join(j)
            x = f'''
                    MATCH (p:Person)
                    WHERE {j}
                    RETURN p
            '''
            return j

    def run_cmd(self, cmd):
        with self.driver.session() as session:
            r = session.run(cmd)
            return self.db_result_format(r)

    
    '''
    def test_api_db(self):

        with Db(self.uri, self.userName, self.password) as db_inst:
            #asserttrue()
    '''
    

    '''
    def test_create(self):
        #check for dups
        #only check names

        for t in self.test_users:
            self.driver.create_user(t)
        for t in self.test_users:
            self.driver.create_user(t)
        
        r = self.run_cmd(self.cmds('match_props', self.test_users))
        self.assertEquals(len(r), len(self.test_users))
    '''

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
    """
    
    """
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

    
    def tearDown(self):
        if self.driver:
            self.driver.close()

        """
        cmd_clean = '''
                        MATCH (all) WHERE all.sig='for_test_db'
                        MATCH ()-[all_r]-() WHERE all_r.sig='for_test_db'                        
                        DELETE all_r
                        DELETE all
                    '''
        

        print('BEFORE CLEAN')
        print('nb_nodes:>' )
        print('nb_relations:>' )
        print('AFTER CLEAN')
        print('nb_nodes:>' )
        print('nb_relations:>' )
        """

if __name__ == '__main__':

    #unitest uses argv, mack sure to remove your own, use -- on yours
    '''
    if len(sys.argv) > 1:
        TestDb.URI = sys.argv.pop()
        TestDb.PASSWORD = sys.argv.pop()
        TestDb.PASSWORD = sys.argv.pop()
    '''
    
    unittest.main()
