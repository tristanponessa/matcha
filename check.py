import string
from PIL import Image
import datetime
import inspect
import sys

from dict_ops import *

#check if someelse exists same pers

def check_age(iage):
    f = [str(n) for n in range(18,100)]
    return iage in f

def check_pwd(ipwd):
    l = (string.ascii_lowercase, string.ascii_uppercase, string.punctuation, string.digits)
    for il in l:
        if len([ch for ch in ipwd if il]) == 0: #at least one of set
            return False
    if len(ipwd) not in range(8,64):
        return False
    
def check_email(x):
    sets_ = (string.ascii_lowercase, string.ascii_uppercase, '+_-!#$&*', string.digits)
    smtp = ('@hotmail', '@outlook', '@gmail')
    ext = ('.com', '.fr')
    email_tags = (f'{_smtp}{_ext}' for _smtp in smtp for _ext in ext) #all combs

    #check end
    if not any([x.endswith(email_tag) for email_tag in email_tags]):
        return False

    x = x.split('@')[0]
    #check 1st part
    if len([ch for ch in x if x not in sets_]) >= 1:
        return False

def check_pic(x):
    try:
        with Image.open(x) as _: pass
        ext = x.split('.')[-1]
        if ext not in ('png', 'jpg', 'jpeg'):
            return False 
    except OSError:
        return False

def check_birthdate(x):
    x = x.split('/')
    if len(x) != 3:
        return False
    day,month,year = *x,
    try :
        datetime.datetime(int(year),int(month),int(day))
    except ValueError :
        return False
    #check with age

def get_all_check_funs():
    check_funs = {}
    cur_file_members = inspect.getmembers(sys.modules[__name__])
    for member in cur_file_members:
        member_name, member_val = *member,
        if member_name.startswith('check'):
            check_funs[member_name] = member_val
    return check_funs

def proform_check_for_key(profile, check_funs, key):
     val = dict_val_similar_key(profile, key)
     check_fun = dict_val_similar_key(check_funs, key)
     return check_fun(val)

def is_correct_profile(profile):
    check_funs = get_all_check_funs()
    if all(proform_check_for_key(profile, check_funs, key) for key in check_funs.keys()):
        return True
    #proform all checks

#check_email('')
#print(check_birthdate('02/2017'))