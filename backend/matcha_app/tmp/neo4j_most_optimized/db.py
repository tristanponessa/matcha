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
        *__var means private access modifier, dont call outside class
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

    def close_db(self):
        self.__driver.close()
        print('closing db')
    
    def __run_cmd(self, cmd):
        with self.__driver.session() as session:
            result_obj =  session.run(cmd)
            result = result_obj.data() #lst of dcts
            self.__log_msg(cmd)
            self.__print_obj_res(result) #cant return data empty
            return result
            
    
    def __log_msg(self, msg):
        print(f'CQL >>> {msg}'.ljust(50))

    
    def __timestamp(self):
        epoch_now = time.time()
        structtime_now = time.localtime(epoch_now)
        format_now = time.strftime("%d/%m/%Y %H:%M:%S", structtime_now)
        return format_now
    
    def __cql_dict(self, d: dict):
        #neo4j proposes a format string with $var instead of {}
        #{'name':'val'} converts to -> {name:'val'}
        dstr = json.dumps(d) #json transforms ' to "
        for k in d.keys():
            dstr = dstr.replace(f'"{k}"', k)
        return dstr
    
    def run_cmd(self, cql_cmd):
        return self.__run_cmd(cql_cmd)
    
    def get_relationship(self, email1, email2):
        #left to right
        cql_cmd = '''
                    MATCH (p:Person) WHERE p.email="{}"
                    MATCH (l:Person) WHERE l.email="{}"
                    MERGE (p)-[r:LIKES]->(l)
                    RETURN p,type(r),l
                  '''.format(email1, email2)
        return self.__run_cmd(cql_cmd) 

    #dont use 
    def fetch_all(self):
        cql_cmd = '''
                    MATCH (all)
                    RETURN all
                  '''
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
                    RETURN *
                  '''.format(email, state)
        return self.__run_cmd(cql_cmd)
    

    def write_msg(self, from_email, to_email, msg):
        cql_cmd = '''
                    MATCH(src:Person) WHERE src.email="{}"
                    MATCH(dst:Person) WHERE dst.email="{}"
                    CREATE (new_msg:Msg{input:"{}", created_on:"{}"})
                    CREATE (src)-[r1:WROTE]->(new_msg)-[r2:DESTINED_TO]->(dst)
                    RETURN src,type(r1),new_msg,type(r2),dst
                  '''.format(from_email, to_email, msg, self.__timestamp())
        return self.__run_cmd(cql_cmd)
    
    def create_user(self, data: dict):
        #merge prevents duplicate creation
        cql_dct_str = self.__cql_dict(data)
        cql_cmd = '''
                    MERGE (new_user:Person{})
                    RETURN new_user
                  '''.format(cql_dct_str)
        return self.__run_cmd(cql_cmd)
    
    def like_user(self, from_email, to_email):
        cql_cmd = '''
                    MATCH (src:Person) WHERE src.email="{}"
                    MATCH (dst:Person) WHERE dst.email="{}"
                    MERGE (src)-[r:LIKES{date:"{}"}]->(dst)
                    RETURN src,type(r),dst
                  '''.format(from_email, to_email, self.__timestamp())
        return self.__run_cmd(cql_cmd)
    
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

        





if __name__ == '__main__':
    #get args
    with Db("bolt://localhost:7687", "neo4j", "0000") as db_inst:
        #db_inst.fetch_all()
        

        #test0 for futur tests create users delete them at end 
        user1 = db_inst.create_user({'name':'crash', 'email':'crash@crapmail.com'})
        user2 = db_inst.create_user({'name':'maria', 'email':'maria@crapmail.com'})

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

        #test4 like 
        db_inst.like_user('crash@crapmail.com', 'maria@crapmail.com')
        r1 = db_inst.get_relationship('crash@crapmail.com', 'crash@crapmail.com')
        r2 = db_inst.get_relationship('maria@crapmail.com', 'crash@crapmail.com')
        print('a relationship? ', r1)
        print('a relationship? ', r2)
        


        #clean up test env
        db_inst.delete_user('crash@crapmail.com')
        db_inst.delete_user('maria@crapmail.com')






        

    


    

    

    
    
    

        




"""


# Execute the CQL query
with graphDB_Driver.session() as graphDB_Session:
    # Create nodes
    graphDB_Session.run(cqlCreate)
   
    # Query the graph    
    nodes = graphDB_Session.run(cqlNodeQuery)
   
    print("List of Ivy League universities present in the graph:")
    for node in nodes:
        print(node)
 
    # Query the relationships present in the graph
    nodes = graphDB_Session.run(cqlEdgeQuery)
   
    print("Distance from Yale University to the other Ivy League universities present in the graph:")
    for node in nodes:
        print(node)

from neo4j import GraphDatabase as neo4j_db

class HelloWorldExample:

    def __init__(self, uri, user, password):
        self.driver = neo4j_db.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]


if __name__ == "__main__":
    greeter = HelloWorldExample("bolt://localhost:7687", "neo4j", "password")
    greeter.print_greeting("hello, world")
    greeter.close()



from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))

def add_friend(tx, name, friend_name):
    tx.run("MERGE (a:Person {name: $name}) "
           "MERGE (a)-[:KNOWS]->(friend:Person {name: $friend_name})",
           name=name, friend_name=friend_name)

def print_friends(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
                         "RETURN friend.name ORDER BY friend.name", name=name):
        print(record["friend.name"])

with driver.session() as session:
    session.write_transaction(add_friend, "Arthur", "Guinevere")
    session.write_transaction(add_friend, "Arthur", "Lancelot")
    session.write_transaction(add_friend, "Arthur", "Merlin")
    session.read_transaction(print_friends, "Arthur")

driver.close()


# import the neo4j driver for Python

from neo4j.v1 import GraphDatabase
 
# Database Credentials
uri             = "bolt://localhost:7687"
userName        = "neo4j"
password        = "test"
 
# Connect to the neo4j database server
graphDB_Driver  = GraphDatabase.driver(uri, auth=(userName, password))
 
# CQL to query all the universities present in the graph
cqlNodeQuery          = "MATCH (x:university) RETURN x"
 
# CQL to query the distances from Yale to some of the other Ivy League universities
cqlEdgeQuery          = "MATCH (x:university {name:'Yale University'})-[r]->(y:university) RETURN y.name,r.miles"
 
# CQL to create a graph containing some of the Ivy League universities
cqlCreate = '''CREATE (cornell:university { name: "Cornell University"}),
(yale:university { name: "Yale University"}),
(princeton:university { name: "Princeton University"}),
(harvard:university { name: "Harvard University"}),
 
(cornell)-[:connects_in {miles: 259}]->(yale),
(cornell)-[:connects_in {miles: 210}]->(princeton),
(cornell)-[:connects_in {miles: 327}]->(harvard),
 
(yale)-[:connects_in {miles: 259}]->(cornell),
(yale)-[:connects_in {miles: 133}]->(princeton),
(yale)-[:connects_in {miles: 133}]->(harvard),
 
(harvard)-[:connects_in {miles: 327}]->(cornell),
(harvard)-[:connects_in {miles: 133}]->(yale),
(harvard)-[:connects_in {miles: 260}]->(princeton),
 
(princeton)-[:connects_in {miles: 210}]->(cornell),
(princeton)-[:connects_in {miles: 133}]->(yale),
(princeton)-[:connects_in {miles: 260}]->(harvard)'''
 
"""