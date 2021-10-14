import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_friendship(self, person1_name, person2_name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_friendship, person1_name, person2_name)
            for record in result:
                print("Created friendship between: {p1}, {p2}".format(
                    p1=record['p1'], p2=record['p2']))

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name):

        # To learn more about the Cypher syntax,
        # see https://neo4j.com/docs/cypher-manual/current/

        # The Reference Card is also a good resource for keywords,
        # see https://neo4j.com/docs/cypher-refcard/current/

        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:KNOWS]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": record["p1"]["name"], "p2": record["p2"]["name"]}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_person(self, person_name):

        def _find_and_return_person(tx, person_name):
        
            query = """
                MATCH (p:Person)
                WHERE p.name = $person_name
                RETURN p.name AS name"""
            
            result = tx.run(query, person_name=person_name)
            return {'name':record["name"] for record in result}

        with self.driver.session() as session:
            result = session.read_transaction(_find_and_return_person, person_name)
            for record in result:
                print("Found person: {record}".format(record=record))
            return result

    def fetch_all(self):
        def fn(tx):
            query = """
                MATCH (n)
                RETURN n AS name"""
            result = tx.run(query)
            return result

        with self.driver.session() as session:
            result = session.read_transaction(fn)
            for record in result:
                continue
                print("Found person: {record}".format(record=record))
            return [record["name"] for record in result]
    
    def fetch_all2(self):
        query = """
            MATCH (n)
            RETURN *"""

        result = None
        with self.driver.session() as session:
            result = session.run(query)
            self.print_obj_res(result)
            return result
    

    def fetch_all_relations(self):
        query = """
            MATCH (p)-[r]-(p2)
            RETURN p,type(r),p2"""

        
        with self.driver.session() as session:
            result = session.run(query)
            self.print_obj_res(result)
            

    
    def copy_res(self, result):
        data = dict()
        for record in result:
            print(record.keys())
            for cql_return_tag in record.keys():
                print('cql return var: ', cql_return_tag)
                #RETURN n becomes a dict {'n':NODES}
                node = record[cql_return_tag]
                data[cql_return_tag] = node

                #print(record.keys())
                #print(type(record['n']))
                print(node.labels, end=' ')
                print(node.items())
            print()

                


    def print_obj_res(self, result):
        
        for record in result:
            print(record.keys())
            for cql_return_tag in record.keys():
                
                print('cql return var: ', cql_return_tag)
                node = record[cql_return_tag]
                #print(record.keys())
                #print(type(record['n']))
                if (isinstance(node,str)):
                    print(node)
                else:
                    print(node.labels, end=' ')
                    print(node.items())
            print()

    

if __name__ == "__main__":
    # See https://neo4j.com/developer/aura-connect-driver/ for Aura specific connection URL.
    scheme = "bolt"  # Connecting to Aura, use the "neo4j+s" URI scheme
    host_name = "localhost"
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "0000"
    app = App(url, user, password)
    #app.create_friendship("Alice", "David")
    #res = app.find_person("Alice")
    #print(res)
    
    
    #res = app.fetch_all2()

    app.fetch_all_relations()
    
    
    app.close()