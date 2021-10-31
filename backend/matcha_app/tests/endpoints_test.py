# Standard library imports
import sys
import time
import logging 
import inspect
import platform
import os
import threading
import unittest

from io import StringIO

# Third party imports
import neo4j
from neo4j import GraphDatabase as neo4j_db
import requests
from flask import request 

#inner project
f = os.path.dirname(__file__)
x = os.path.join(f, '..')
sys.path.append(x)
import db
import endpoints
import app
from fields import *


class Test(unittest.TestCase):

    def setUp(self):
        self.app_inst = app.App('bolt://localhost:7687', 'neo4j', '0000')
        self.app_inst.app_obj.testing = True
        self.app_test = self.app_inst.app_obj.test_client()  #prevents flask from overriding the test module 

    def test_home(self):
        #result = self.app_test.get('/signup')
        correct = {
        'email' : Email.random_(),
        'pwd' : Pwd.random_(),
        'name' : FirstName.random_(),
        'last_name' : LastName.random_(),
        'birthdate' : Birthdate.random_(),
        'location' : Location.random_(),
        'tags' : Tags.random_(),
        'intro' : Intro.random_(),
        'pics' : Pics.random_(),
        'gender' : Gender.random_(),
        'sex_ori' : SexOrientation.random_(),
        }
        
        '''
        base_url = request.base_url
        self.print_debug(base_url)
        url = base_url + self.app_inst.endpoints_obj.rules['sign_up']['url']
        self.print_debug(url)
        correct_rjson = self.app_test.post(url, data=correct) #auto calls self.signup()
        
        #self.print_debug(dir(self.app_test))
        self.print_debug(correct_rjson)

        '''
        res = self.app_test.post('/signup', data={'name':'crash'})
        self.print_debug(res)
        self.print_debug(dir(res))
        self.print_debug(res.json)
        # Make your assertions
    
    
    def print_debug(self, msg, override=False):
        
        #to print in testttest
        logging.basicConfig(stream=sys.stdout)
        log = logging.getLogger("TestDb")
        log.setLevel(logging.DEBUG)
        log.debug(msg)
    
   
    
'''
def test_1_signup_RULE(self):
        test_nickname = 'test_signup'  #no way to get name of fun in fun
        err_msgs = []

        correct = {
        'email' : Email.random_(),
        'pwd' : Pwd.random_(),
        'name' : FirstName.random_(),
        'last_name' : LastName.random_(),
        'birthdate' : Birthdate.random_(),
        'location' : Location.random_(),
        'tags' : Tags.random_(),
        'intro' : Intro.random_(),
        'pics' : Pics.random_(),
        'gender' : Gender.random_(),
        'sex_ori' : SexOrientation.random_(),
        }

        uncomplete = correct.copy()
        del uncomplete['tags']

        incorrect = correct.copy()
        incorrect['birthdate'] = '22/22/1922'

        malicious = correct.copy()
        malicious['name'] = "match (n) return n" #cql code


        self.app.endpoints_obj.signup()
        url = self.app.endpoints_obj.rules['sign_up']


        correct_rjson = requests.post(url, data=correct)
        uncorrect_rjson = requests.post(url, data=uncorrect)
        incorrect_rjson = requests.post(url, data=incorrect)
        malicious_rjson = requests.post(url, data=malicious)

        #return msg
        #if in db 
        if correct_rjson['success'] == False:
            err_msg.append(rjson)
        if uncorrect_rjson['success']:
            err_msg.append(uncorrect_rjson)
        if incorrect_rjson['success']:
            err_msg.append(incorrect_rjson)
        if malicious_rjson['success']:
            err_msg.append(malicious_rjson)
        
        self.error_msgs[test_nickname] = err_msgs
        return len(err_msgs) > 0     
'''

if __name__ == '__main__':

    #testtest uses argv, mack sure to remove your own, use -- on yours
    '''
    if len(sys.argv) > 1:
        TestDb.URI = sys.argv.pop()
        TestDb.PASSWORD = sys.argv.pop()
        TestDb.PASSWORD = sys.argv.pop()
    '''
    unittest.main()
    

    #['cql': 'file', 'tested_module': 'file', 'exceptions']
    #with Test("bolt://localhost:7687", "neo4j", "0000", True) as test_session:
    #    test_session.run_tests()


