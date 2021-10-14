import sys
import time
import json
#sys.path.append('/home/user/Documents/coding/matcha')
#sys.path.append('/home/user/Documents/coding/matcha/matcha_app')
#sys.path.append('/home/user/Documents/coding/matcha/matcha_app/db_files')

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
        print('closing db')
        self.__driver.close()
    
    def __run_cmd(self, fn, cmd):
        with self.__driver.session() as session:
            #session.write_transaction(create_friend_of, "Alice", "Carl")
            return session.run(cmd)
    
    def __timestamp(self):
        epoch_now = time.time()
        structtime_now = time.localtime(epoch_now)
        format_now = time.strftime("%d/%m/%Y %H:%M:%S", structtime_now)
        return format_now
    
    def __cql_dict(self, d: dict):
        #{'name':'val'} converts to -> {name:'val'}
        dstr = json.dumps(d) #json transforms ' to "
        for k in d.keys():
            dstr = dstr.replace(f'"{k}"', k)
        return dstr

    #dont use 
    def fetch_all(self):
        cql_cmd = '''
                    MATCH (all)
                    RETURN all
                  '''
        return self.__run_cmd(cql_cmd)
    
    
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
        cql_dct_str = self.__cql_dict(data)
        cql_cmd = '''
                    CREATE (new_user:Person{})
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





if __name__ == '__main__':
    #get args
    with Db("bolt://localhost:7687", "neo4j", "0000") as db_inst:
        print('welcome')
        """
        x = db_inst.create_user({'name':'jejis', 'id':7879})
        all_data = db_inst.fetch_all()
        
        print(all_data)
        print(x.keys())
        print(x.values())
        print(x['new_user'])

        print(all_data.values())
        print(type(all_data.keys()))

        for data in all_data:
            print(data)
        """

    


    

    

    
    
    

        




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