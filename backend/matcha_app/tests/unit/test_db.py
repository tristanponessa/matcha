import unittest
from neo4j import GraphDatabase as neo4j_db


#def print_cql:
#def print_res:




class TestDb(unittest.TestCase):

    def setUp(self, uri, userName, password):
        self.uri = uris
        self.userName = userName
        self.password = password
        self.sig = 'for_test_db' #signature for db elem
        self.driver = neo4j_db.driver(uri, auth=(userName, password))
        self.cql_get_test_nodes = f'''MATCH (all) WHERE all.sig='{self.sig}'
                                         RETURN count(all)
                                      '''
        self.cql_get_test_relations = f'''MATCH ()-[all_r]-() WHERE all_r.sig='{self.sig}'
                                      RETURN count(all_r) '''
        


        self.test_users = []
        self.test_users.append({'sig':self.sig, 'name':'crash', 'email':'crash@crapmail.com', 'born':'27/02/1996', 'sex_ori':'female','ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'crash', 'email':'crash_2@crapmail.com' , 'born':'27/02/1996', 'sex_ori':'female', 'ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'crash', 'email':'bad@crapmail.com' , 'born':'27/02/1996', 'sex_ori':'female', 'ban':'true'})
        self.test_users.append({'sig':self.sig, 'name':'maria', 'email':'maria@crapmail.com', 'born':'10/04/1994', 'sex_ori':'male','ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'exodia', 'email':'exodia@dumpmail.com', 'born':'01/01/1996', 'sex_ori':'female','ban':'false'})
        self.test_users.append({'sig':self.sig, 'name':'iswear', 'email':'iswear@dumpmail.com', 'born':'02/07/1999', 'sex_ori':'male female','ban':'false'})

        


    def run_cmd(self, cmd):
        with self.driver.session() as session:
            return session.run(cmd)
        

    def test_db(self):
        with Db(self.uri, self.userName, self.password) as db_inst:
            #asserttrue()


    def test_create(self):
        #check for dups

        for t in test_users:
            db_inst.create_user(t)
        for t in test_users:
            db_inst.create_user(t)
        all = db_inst.fetch_all() 
        print(len(all))
        #assertequals(len(test_users) == len(all))

    def test_ban(self):
        print(db_inst.user_exists('crash@crapmail.com'))

                #test2 create ban check_if_banned delte search
                db_inst.create_user({'name':'Bad', 'email':'bad@crapmail.com'})
                print(db_inst.user_exists('bad@crapmail.com'))
                db_inst.ban_user('bad@crapmail.com', 'true')
                print(db_inst.user_exists('bad@crapmail.com'))
                db_inst.delete_user('bad@crapmail.com')
                print(db_inst.user_exists('bad@crapmail.com'))

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
    
    def test_like(self):
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
    
    def test_write(self):

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
    

    def test_sort_filter():
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
        

    
    def tearDown(self):
        self.driver.close()


        print('BEFORE CLEAN')
        print('nb_nodes:>' )
        print('nb_relations:>' )
        print('AFTER CLEAN')
        print('nb_nodes:>' )
        print('nb_relations:>' )


if __name__ == '__main__':
    unittest.main()
