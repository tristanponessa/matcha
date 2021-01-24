import requests
import unittest
import sys

from app_ import *
from matcha_app.sqlite_db import *
from matcha_app.dict_ops import *
from matcha_app.zemail import *

class TestManager(unittest.TestCase):

    def setUp(self):
        self.domain = 'http://127.0.0.1:5000/'
        self.json_headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        launch_flask()

    def test_home_page(self):

        #db_manager()
        #flask run
        #

        #payload = open("request.json")
        #headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        #r = requests.get(url, data=payload, headers=headers)
        rjson = requests.get(self.domain)
        self.assertTrue('msg' in rjson)

    """
    def test_signup_page(self):
        endpoint = self.domain + 'signup'
        correct_user_json = {'email' : 'tv@hotmail.com', 'pwd' : '1Aa*1234'}
        false_email_user_json = {'email': '@@hotmail...com', 'pwd': '1Aa*1234'}
        false_pwd_user_json = {'email': 'tv@hotmail.com', 'pwd': '1234'}
        false_both_user_json = {'email': '@hotmail', 'pwd': '1234'}

        #get
            get_json = requests.get(self.domain)
            self.assertTrue('msg' in get_json)
        #post

            post_json = requests.post(self.domain, data=correct_user_json, headers=self.json_headers)

            
            self.assertTrue(profile_exists())



        # payload = open("request.json")
        # headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        # r = requests.get(url, data=payload, headers=headers)
        rjson = requests.get(self.domain)
        self.assertTrue('msg' in rjson)
    """





"""

if __name__ == '__main__':
    unittest.main()
"""