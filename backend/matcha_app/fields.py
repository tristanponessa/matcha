import string
import time
from PIL import Image
import datetime
import inspect
import sys
import string
import os
import random #seed gens specific nbs, scope changing resets and repeats the pattern, we must design a project seed and for every rand call we add a new seed
from datetime import datetime
from dateutil.relativedelta import relativedelta 


str_symbs = '+_-!#$&*'
punctuation = '!#$%&()*+,-./:;<=>?@[\]^_{|}~'

def gen_rand_profiles(n, seed_=0):
    #for seed x: x -> x + n
    
    users = []
    for i in range(n):
        user = {
        'email' : Email.random_(n),
        'pwd' : Pwd.random_(n + 1),
        'name' : FirstName.random_(n + 2),
        'last_name' : LastName.random_(n + 3),
        'birthdate' : Birthdate.random_(n + 4),
        'location' : Location.random_(n + 5),
        'tags' : Tags.random_(n + 6),
        'intro' : Intro.random_(n + 7),
        'pics' : Pics.random_(n + 8),
        'gender' : Gender.random_(n + 9),
        'sex_ori' : SexOrientation.random_(n + 10),
        'banned' : Blocked.random_(n + 11),
        'account_activated' : Activated.random_(n + 12)
        }
        users.append(user)

    n = 12
    all_emails = [d['email'] for d in users]
    for user in users:
        user['msgs'] = Msgs.random_(all_emails, n)
        user['likes'] = Likes.random_(all_emails, n)
        n += 1
    
    return users


def rand_seed():
    return random.randint(0,999999)

def gen_rand_string(start, end, chs, seed_=rand_seed()):
    random.seed(seed_)
    return ''.join((random.choice(chs) for _ in range(start, end)))

def is_subdct(sub_dct, dct, exact_value=True):
    match = 0
    for k, v in sub_dct.items():
        if  (exact_value and k in dct and dct[k] == v) or \
            (k in dct and v in dct[k]):
            match += 1
    if len(sub_dct) == match:
        return True


class Random:
    #everytime a rand fn is called, the seed must increase once

    _seed_nb = 0

    def	get_seed():
        Random._seed_nb += 1
        return Random._seed_nb

    def rand(lst=None):
        random.seed(Random.get_seed())
        return random.choice(lst)

        
        


class FirstName(Random):
    access = ['user_modify']

    def random_(seed_=rand_seed()):
        random.seed(seed_)
        first = random.choice(string.ascii_uppercase)
        rest = gen_rand_string(3, 8, string.ascii_lowercase, seed_)
        return first + rest

class LastName(Random):

    access = ['user_modify']

    def random_(seed_=rand_seed()):
        random.seed(seed_)
        first = random.choice(string.ascii_uppercase)
        rest = gen_rand_string(8, 12, string.ascii_lowercase, seed_)
        return first + rest


class Time(Random):

    def time_diff(t1, t2, type):
        if type == 'timestamp':
            fmt = '%Y-%m-%d %H:%M:%S'
        if type == 'birthdate':
            fmt = '%Y-%m-%d'
        d1 = datetime.strptime(t1, fmt)
        d2 = datetime.strptime(t2, fmt)
        time_difference = relativedelta(d2, d1)
        return time_difference.years


class Timestamp(Time, Random):
    access = []

    def get_now_time():
        epoch_now = time.time()
        structtime_now = time.localtime(epoch_now)
        format_now = time.strftime("%d/%m/%Y %H:%M:%S", structtime_now)
        return format_now

    def random_(seed_=rand_seed()):  # do not assign to rand list
        random.seed(seed_)
        day = random.randint(1, 28)
        month = random.randint(1, 12)
        year = random.randint(2001, 2020)
        hour = random.randint(0, 23)
        min_ = random.randint(0, 59)
        sec = random.randint(0, 59)
        return f'{year}-{month:02d}-{day:02d} {hour:02d}:{min_:02d}:{sec:02d}'

class Birthdate(Time, Random):
    #2039-07-14
    access = ['user_modify', 'matcha_cmp']

    def check_age(age):
        return int(age) in range(18, 100)

    def check(x):
        x = x.split('-')
        if len(x) != 3:
            return False
        day, month, year = x
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            return False
        # check with age

    def same_age_range(b1, b2):
        year1 = b1.split('-')[0]
        year2 = b2.split('-')[0]
        return abs(int(year1) - int(year2)) <= 5

    def diff(b1, b2):
        b1 = b1.split('-')
        b2 = b2.split('-')





    def random_(seed_=rand_seed()):
        random.seed(seed_)
        day = random.randint(1, 28)
        month = random.randint(1, 12)
        year = random.randint(1955, 2000)
        return f'{year}-{month}-{day}'

    def sort_(profile):
        return datetime.strptime(profile['birthdate'], '%d/%m/%Y')





class Pics(Random):

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

    
    def random_(seed_=rand_seed()):
        random.seed(seed_)
        url = './matcha_app/static/pics'
        pics = os.listdir(url)
        nb = random.randint(1, 4)
        p = {'others': []}
        for i in range(nb):
            r = random.randint(0, len(pics) - 1)
            if i == 0:
                p['profile_pic'] = f'{url}/{pics[r]}'
            else:
                p['others'].append(f'{url}/{pics[r]}')
        return p


class Email(Random):
    access = ['user_modify']

    smtp = ('@hotmail', '@outlook', '@gmail')
    smpt_ext = ('.com', '.fr')
    email_tags = (f'{_smtp}{_ext}' for _smtp in smtp for _ext in smpt_ext)

    def random_(seed_=rand_seed()):
        random.seed(seed_)
        r = random.choice

        user_set = string.ascii_letters + '_'
        smtp = ('@hotmail', '@outlook', '@gmail')
        ext = ('.com', '.fr')

        rid = ''.join((r(user_set) for _ in range(random.randint(1, 25))))
        rand_email = rf'{rid}{r(smtp)}{r(ext)}'

        return rand_email


    def check(x):
        sets_ = (string.ascii_lowercase, string.ascii_uppercase, '+_-!#$&*', string.digits)
        smtp = ('@hotmail', '@outlook', '@gmail')
        ext = ('.com', '.fr')
        email_tags = (f'{_smtp}{_ext}' for _smtp in smtp for _ext in ext)  # all combs

        # check end
        if any([(x and x.endswith(email_tag)) for email_tag in email_tags]):
            return True



class Pwd(Random):

    access = ['user_modify']
    pwd_len = range(8, 64)
    pwd_str = (string.ascii_lowercase, string.ascii_uppercase, string.punctuation, string.digits)

    def random_(seed_=rand_seed()):
        random.seed(seed_)
        punctuation = '!#$%&()*+,-./:;<=>?@[\]^_{|}~'
        all_ = string.ascii_letters + punctuation + string.digits
        rpwd = ''.join((random.choice(all_) for _ in range(random.randint(8, 64))))
        return rpwd

    def check(ipwd):
        l = (string.ascii_lowercase, string.ascii_uppercase, string.punctuation, string.digits)
        for il in l:
            if len([ch for ch in ipwd if il]) == 0:  # at least one of set
                return False
        if len(ipwd) not in range(8, 64):
            return False

class SexOrientation(Random):

    access = ['user_modify', 'matcha_cmp']

    def random_(seed_=rand_seed()):
        random.seed(seed_)
        x = ('male', 'female', 'male female')
        return random.choice(x)

    def cmp(p1, p2):
        #profile
        pref1 = p1['sex_ori']
        gender1 = p1['gender']
        pref2 = p2['sex_ori']
        gender2 = p2['gender']
        return gender1 in pref2 and gender2 in pref1

class Location(Random):

    access = ['user_modify', 'matcha_cmp']

    def random_(seed_=rand_seed()):
        random.seed(seed_)
        locs = ('USA', 'France', 'Moon', 'Spain', 'Canada', 'Turkey', 'Mexico')
        return random.choice(locs)
        # pip install flask-simple-geoip

    def cmp_(p1, p2):
        return p1['location'] == p2['location']

class Tags(Random):

    access = ['user_modify', 'matcha_cmp']
    tags = ('drawing','coding','politics','chess','sports','workout','sleeping',
            'skydiving','movies','reading','creating','cooking','dancing','driving','travel')

    def random_(seed_=rand_seed()):
        random.seed(seed_)
        
        rnb = random.randint(0, len(Tags.tags))
        rtags = [random.choice(Tags.tags) for i in range(rnb)]
        return list(set(rtags)) #remove duplicates

    def cmp_(p1, p2):
        v1 = p1['tags']
        v2 = p2['tags']
        return len(set(v1) & set(v2)) > 0  # intersection keep all eq


class Gender(Random):

    access = ['user_modify']

    def random_(seed_=rand_seed()):
        random.seed(seed_)
        x = ('male', 'female')
        return random.choice(x)

class Intro(Random):

    def random_(seed_=rand_seed()):
        random.seed(seed_)
        nb_words = random.randint(0, 20)
        intro = ''
        for i in range(nb_words):
            len_word = random.randint(1, 10)
            word = ''.join((random.choice(string.ascii_lowercase) for _ in range(len_word)))
            intro += f' {word} '
        return intro

class Msgs(Random):

    access = ['user_modify']

    def random_(emails, seed_=rand_seed()):
        random.seed(seed_)
        rnb = random.randint(0, len(emails))
        msgs = []
        for _ in range(rnb):
            msg = dict()
            msg['date'] = Timestamp.random_(seed_ + 5)
            msg['to_email'] = random.choice(emails)  # can send to himself
            msg['msg'] = Intro.random_(seed_ + 10)
            seed_ += 1
            msgs.append(msg)
        return msgs

class Likes(Random):

    access = ['user_modify']

    def random_(emails, seed_):
        random.seed(seed_)
        rnb = random.randint(0, len(emails))
        return [random.choice(emails) for i in range(rnb)]

class Activated(Random):

    access = ''

    def random_(seed_=rand_seed()):
        random.seed(seed_)
        return random.choice([True, False])

class Blocked(Random):

    access = ''

    def random_(seed_=rand_seed()):
        random.seed(seed_)
        return random.choice([True, False])




    """
    if which == 'cmp':
        return {clsname:clsobj.cmp_ for clsname,clsobj in clss}
    if which == 'random':
        return {clsname: clsobj.random_ for clsname, clsobj in clss}
    if which == 'check':
        return {clsname: clsobj.cmp_ for clsname, clsobj in clss}
    """



if __name__ == '__main__':
    pros = gen_rand_profiles(10)
    for i,p in enumerate(pros):
        print(f'profile {i}')
        for k,v in p.items():
            if k == 'msgs':
                print('    msgs :')
                for msg in v:
                    for k,v in msg.items():
                        print(f'        {k} {v}')
            elif k == 'likes':
                print('    likes :')
                for like in v:
                        print(f'        {like}')
            else:
                print(f'    {k} : {v}')
        print('\n' * 3)




