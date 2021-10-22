#clean user data funs
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer)
from itsdangerous.exc import SignatureExpired
from flask import Markup

site_secret_key = 'WEBSITE_SECRET_KEY'

def gen_unik_token(email):
    s = Serializer(site_secret_key, 60 * 30)  # 60 secs by 30 mins
    token = s.dumps({'email': email}).decode('utf-8')  # encode user id
    return token

def get_token_data(token):
    s = Serializer(site_secret_key)
    try:
        return s.loads(token)['email']
    except SignatureExpired:
        return 'expired'
    except KeyError:
        return 'no email key'

def clean_user_data(data):
    #check sql commands
    """
    clean_data = {}
    for k,v in data.items():
        if v is None:
            v = ''
        clean_data[k] = escape(v)
    """
    return data

#stop sql injection test
#cross site attack
#js atk
#...