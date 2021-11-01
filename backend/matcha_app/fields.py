import string
import time
import datetime
import inspect
import sys
import string
import os
import random #seed gens specific nbs, scope changing resets and repeats the pattern, we must design a project seed and for every rand call we add a new seed
from datetime import datetime

from dateutil.relativedelta import relativedelta 
from PIL import Image


str_symbs = '+_-!#$&*'
punctuation = '!#$%&()*+,-./:;<=>?@[\]^_{|}~'
sign_up_fields = ['email', 'pwd', 'name', 'last_name', 'birthdate', 'location', 'tags', 'intro', 'pics', 'gender', 'sex_ori']
max_input_size = 50

def gen_rand_profiles(n):
    #for seed x: x -> x + n
    
    users = []
    for i in range(n):
        user = {
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
        'banned' : Blocked.random_(),
        'account_activated' : Activated.random_()
        }
        users.append(user)

    all_emails = [d['email'] for d in users]
    for user in users:
        user['msgs'] = MsgManager.random_(all_emails)
        user['likes'] = Likes.random_(all_emails)
    
    return users


def is_profile(data):

    if  (not data) or \
        (list(data.keys()).sort() != sign_up_fields.sort()):
        return False #data missing
    
    checks = {
    'email' : Email.check_(),
    'pwd' : Pwd.check_(),
    'name' : FirstName.check_(),
    'last_name' : LastName.check_(),
    'birthdate' : Birthdate.check_(),
    'location' : Location.check_(),
    'tags' : Tags.check_(),
    'intro' : Intro.check_(),
    'pics' : Pics.check_(),
    'gender' : Gender.check_(),
    'sex_ori' : SexOrientation.check_(),
    }

    with open('C:/Users/trps/Documents/my_stuff/coding/matcha/backend/matcha_app/tests/test_outputs/tested_module_output.txt', 'a') as f: 
        f.writelines(['55'])

    if all(checks.values()) == False:
        return False
    return True




class Random:
    #everytime a rand fn is called, the seed must increase once

    _seed_nb = 0

    def	get_seed():
        Random._seed_nb += 1
        return Random._seed_nb

    def rand(lst):
        random.seed(Random.get_seed())
        return random.choice(lst)

    def rand_str(lst, start, end):
        rlen = Random.rand(range(start, end))
        rlst = random.sample(lst, rlen)
        return ''.join(rlst)
        #return ''.join([Random.rand(lst) for _ in range(0, rlen)])
    
    def rand_lst(lst, start, end):
        rlen = Random.rand(range(start, end))
        return random.sample(lst, rlen)
        #return [Random.rand(lst) for _ in range(0, rlen)]



class FirstName:
    access = ['user_modify']

    def random_():
        first = Random.rand(string.ascii_uppercase)
        rest = Random.rand_str(string.ascii_lowercase, 3, 8)
        return first + rest
    
    def check_(name):
        #check if each ch isiin the set
        if ()
        if all()



class LastName:

    access = ['user_modify']

    def random_():
        first = Random.rand(string.ascii_uppercase)
        rest = Random.rand_str(string.ascii_lowercase, 8, 12)
        return first + rest


class Time:

    def time_diff(t1, t2, type):
        if type == 'timestamp':
            fmt = '%Y-%m-%d %H:%M:%S'
        if type == 'birthdate':
            fmt = '%Y-%m-%d'
        d1 = datetime.strptime(t1, fmt)
        d2 = datetime.strptime(t2, fmt)
        time_difference = relativedelta(d2, d1)
        return time_difference.years
    
    def timestr_to_epoch(s1):
        fmt = '%Y-%m-%d %H:%M:%S'
        return datetime.strptime(s1, fmt).timestamp()


class Timestamp:
    access = []

    def get_now_time():
        epoch_now = time.time()
        structtime_now = time.localtime(epoch_now)
        format_now = time.strftime("%d/%m/%Y %H:%M:%S", structtime_now)
        return format_now

    def random_():  # do not assign to rand list
        
        day = Random.rand(range(1, 28))
        month = Random.rand(range(1, 12))
        year = Random.rand(range(2001, 2020))
        hour = Random.rand(range(0, 23))
        min_ = Random.rand(range(0, 59))
        sec = Random.rand(range(0, 59))
        return f'{year}-{month:02d}-{day:02d} {hour:02d}:{min_:02d}:{sec:02d}'

class Birthdate:
    #2039-07-14
    access = ['user_modify', 'matcha_cmp']

    def check_age(age):
        return int(age) in range(18, 100)

    def check(x):
        x = x.split('-')
        if len(x) != 3:
            return False
        year, month, day = x
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            return False
        return True
        # check with age

    def same_age_range(b1, b2):
        year1 = b1.split('-')[0]
        year2 = b2.split('-')[0]
        return abs(int(year1) - int(year2)) <= 5

    def diff(b1, b2):
        b1 = b1.split('-')
        b2 = b2.split('-')

    def random_():
        day = Random.rand(range(1, 28))
        month = Random.rand(range(1, 12))
        year = Random.rand(range(1955, 2000))
        return f'{year}-{month}-{day}'

    def sort_(profile):
        return datetime.strptime(profile['birthdate'], '%d/%m/%Y')





class Pics:

    access = ['user_modify']
    pic_ext = ('png', 'jpg', 'jpeg')

    def check(x):
        try:
            with Image.open(x) as _:
                pass
            ext = x.split('.')[-1]
            if ext not in ('png', 'jpg', 'jpeg'):
                return False
        except OSError:
            return False
        return True

    
    def random_():
        
        url = './matcha_app/static/pics'
        pics = os.listdir(url)
        nb = Random.rand(range(1, 4))
        p = {'others': []}
        for i in range(nb):
            r = Random.rand(range(0, len(pics) - 1))
            if i == 0:
                p['profile_pic'] = f'{url}/{pics[r]}'
            else:
                p['others'].append(f'{url}/{pics[r]}')
        return p


class Email:
    access = ['user_modify']

    smtp = ('@hotmail', '@outlook', '@gmail')
    smpt_ext = ('.com', '.fr')
    email_tags = (f'{_smtp}{_ext}' for _smtp in smtp for _ext in smpt_ext)

    def random_():
        
        user_set = string.ascii_letters + '_'
        smtp = ('hotmail', 'outlook', 'gmail')
        ext = ('com', 'fr')

        rname = Random.rand_str(user_set, 1, 25)
        rsmtp = Random.rand(smtp)
        rext =  Random.rand(ext)
        rand_email = f'{rname}@{rsmtp}.{rext}'
        return rand_email


    def check(x):
        sets_ = (string.ascii_lowercase, string.ascii_uppercase, '+_-!#$&*', string.digits)
        smtp = ('@hotmail', '@outlook', '@gmail')
        ext = ('.com', '.fr')
        email_tags = (f'{_smtp}{_ext}' for _smtp in smtp for _ext in ext)  # all combs

        # check end
        if any([(x and x.endswith(email_tag)) for email_tag in email_tags]):
            return True



class Pwd:

    access = ['user_modify']
    pwd_len = range(8, 64)
    pwd_str = (string.ascii_lowercase, string.ascii_uppercase, string.punctuation, string.digits)

    def random_():
        
        punctuation = '!#$%&()*+,-./:;<=>?@[\]^_{|}~'
        all_ = string.ascii_letters + punctuation + string.digits
        rpwd = Random.rand_str(all_, 12, 32)
        return rpwd

    def check(ipwd):
        l = (string.ascii_lowercase, string.ascii_uppercase, string.punctuation, string.digits)
        for il in l:
            if len([ch for ch in ipwd if il]) == 0:  # at least one of set
                return False
        if len(ipwd) not in range(8, 64):
            return False

class SexOrientation:

    access = ['user_modify', 'matcha_cmp']

    def random_():
        
        x = ('male', 'female', 'male female')
        return Random.rand(x)

    def cmp(p1, p2):
        #profile
        pref1 = p1['sex_ori']
        gender1 = p1['gender']
        pref2 = p2['sex_ori']
        gender2 = p2['gender']
        return gender1 in pref2 and gender2 in pref1

class Location:

    access = ['user_modify', 'matcha_cmp']

    def random_():
        
        locs = ('USA', 'France', 'Moon', 'Spain', 'Canada', 'Turkey', 'Mexico', 'Atlantis')
        return Random.rand(locs)
        # pip install flask-simple-geoip

    def cmp_(p1, p2):
        return p1['location'] == p2['location']

class Tags:

    access = ['user_modify', 'matcha_cmp']
    tags = ('drawing','coding','politics','chess','sports','workout','sleeping',
            'skydiving','movies','reading','creating','cooking','dancing','driving','travel')

    def random_():
        rtags = Random.rand_lst(Tags.tags, 0, len(Tags.tags))
        return list(set(rtags)) #remove duplicates

    def cmp_(p1, p2):
        v1 = p1['tags']
        v2 = p2['tags']
        return len(set(v1) & set(v2)) > 0  # intersection keep all eq


class Gender:

    access = ['user_modify']

    def random_():
        
        x = ('male', 'female')
        return Random.rand(x)

class Intro:

    def random_():
        
        nb_words = Random.rand(range(0, 20))
        intro = ''
        for i in range(nb_words):
            word = Random.rand_str(string.ascii_lowercase, 1, 8)
            intro += f' {word} '
        return intro


class Msg:

    def __init__(self, a, b:str, c, d):
        self.to_email = a
        self.date = b
        self.input = c
        self.new = d
    
    def __gt__(self, other):
        #for built in list.sort
        a = Time.timestr_to_epoch(self.date)
        b = Time.timestr_to_epoch(other.date)
        return b < a
    
    def __repr__(self):
        to_email = self.to_email.ljust(50)
        date = self.date.ljust(20)
        input_ = self.input
        return f'msg> TO_EMAIL: {to_email} DATE: {date} INPUT: {input_}'
    
    def to_dct(self):
        return self.__dict__

    @staticmethod
    def random_(emails):
        remail = Random.rand(emails)
        rdate = Timestamp.random_()
        rinput = Intro.random_()
        rnew = Random.rand([True, False])
        return Msg(remail, rdate, rinput, rnew)


class MsgManager:

    access = ['user_modify']

    def random_(emails):
        rnb = Random.rand(range(0, 10)) #talked to up to 10 diff poeple
        msgs = []
        for _ in range(rnb):
            remail = Random.rand(emails)
            rnmsgs = Random.rand(range(1,50)) #wrote n msgs
            msgs.append(Msg.random_(emails))
        print(msgs)
        msgs.sort()
        return msgs # sorts by Msg.__gt__
    
    
    
    '''
    def sort_(lst, key='date'):
        if key == 'date':
            lst = lst.sort()
        if key == 'to_email':
            lst = lst.sort(key=lambda msg: msg.to_email)
        return lst

    def filter_(lst, key):
    '''



class Likes:

    access = ['user_modify']

    def __init__(self, to_email, date):
        self.date = date
        self.to_email = to_email
    
    def __gt__(self, other):
        #for built in list.sort
        a = Time.timestr_to_epoch(self.date)
        b = Time.timestr_to_epoch(other.date)
        return b < a

    def __repr__(self):
        to_email = self.to_email.ljust(50)
        date = self.date.ljust(20)
        return f'like> EMAIL: {to_email} LIKED_THE:{date}'

    @staticmethod
    def random_(emails):
        emails = Random.rand_lst(emails, 0, 10)
        lst = []
        for e in emails:
            lst.append(Likes(e, Timestamp.random_()))
        lst.sort()
        return lst

class Activated:

    access = ''

    def random_():
        return Random.rand([True, False])

class Blocked:

    access = ''

    def random_():
        
        return Random.rand([True, False])




    """
    if which == 'cmp':
        return {clsname:clsobj.cmp_ for clsname,clsobj in clss}
    if which == 'random':
        return {clsname: clsobj.random_ for clsname, clsobj in clss}
    if which == 'check':
        return {clsname: clsobj.cmp_ for clsname, clsobj in clss}
    """




if __name__ == '__main__':
    is_profile({'a': 55})
    
    
    






