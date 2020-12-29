import string

from PIL import Image
import datetime 

def check_age(iage):
    f = [str(n) for n in range(18-100)]
    return iage in f

def check_pwd(ipwd):
    l = (string.ascii_lowercase, string.ascii_uppercase, string.punctuation, string.digits)
    for il in l:
        if len((ch for ch in ipwd if il)) == 0: #at least one of set
            return False
    if len(ipwd) not in range(8-64):
        return False
    
def check_email(x):
    sets_ = (string.ascii_lowercase, string.ascii_uppercase, '+_-!#$&*', string.digits)
    smtp = ('@hotmail', '@outlook', '@gmail')
    ext = ('.com', '.fr')
    email_tags = (f'{_smtp}{_ext}' for _smtp in smtp for _ext in ext) #all combs

    #check end
    if not any((x.endswith(email_tag) for email_tag in email_tags)):
        return False

    x = x.split('@')[0]
    #check 1st part
    if len((ch for ch in x if x not in sets_)) >= 1:
        return False

def check_pic(x):
    try:
        with Image.open(x) as _: pass
    except OSError:
        return False

def check_birthdate(x):
    """
    x = x.split('/')
    if len((_x for _x in x if len(_x) == 2)) != 3
        return False
    if len((_x for _x in x if len(_x) == 2)) != 3
        return False
    """
    x = x.split('/')
    if len(x) != 3:
        return False
    day,month,year = *x,
    try :
        datetime.datetime(int(year),int(month),int(day))
    except ValueError :
        return False
    #check with age
    

check_email('')
print(check_birthdate('02/2017'))


