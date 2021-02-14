import string
import time
from PIL import Image
import datetime
import inspect
import sys
import string
import os
import random


symbs = '+_-!#$&*'
sets_ = (string.ascii_lowercase, string.ascii_uppercase, symbs, string.digits)
nosymbs_str = string.ascii_lowercase + string.ascii_uppercase + string.digits


def gen_rand_nosymbs(len) -> str:
    return ''.join((random.choice(nosymbs_str) for _ in range(len)))

def gen_rand_chs(len, chs: str) -> str:
    return ''.join((random.choice(chs) for _ in range(len)))


def is_subdct(sub_dct, dct):
    match = 0
    for k, v in sub_dct.items():
        if k in dct and dct[k] == v:
            match += 1
    if len(sub_dct) == match:
        return True

def create_profiles(master_seed):

    nb_users = 10
    min_seed = 0#(nb_users * master_seed)
    max_seed = 99999#min_seed + nb_users

    profiles = []  # to put into db list of dicts
    seed_nbs = tuple(random.randint(0,9999) for _ in range(nb_users))
    emails = tuple(Email.random_(seednb) for seednb in seed_nbs)
    field_fns = get_field_fns('random_')

    for seed_nb, email in zip(seed_nbs, emails):
        profile = {'email' : email}
        for clsname, randfn in field_fns.items():
            if clsname != 'Email':
                if randfn.__code__.co_argcount == 2:
                    profile[clsname.lower()] = randfn(emails, seed_nb)
                else:
                    profile[clsname.lower()] = randfn(seed_nb)
        profiles.append(profile)
    return profiles

class Timestamp:
    access = []

    def get_now_time():
        epoch_now = time.time()
        structtime_now = time.localtime(epoch_now)
        format_now = time.strftime("%d/%m/%Y %H:%M:%S", structtime_now)
        return format_now

    def random_(seed_):  # do not assign to rand list
        # random.seed(seed_)
        day = random.randint(1, 28)
        month = random.randint(1, 12)
        year = random.randint(2001, 2020)
        hour = random.randint(0, 23)
        min_ = random.randint(0, 59)
        sec = random.randint(0, 59)
        return f'{day:02d}/{month:02d}/{year} {hour:02d}:{min_:02d}:{sec:02d}'



class FirstName:
    access = ['user_modify']

    def random_(seed_):
        # random.seed(seed_)
        x = random.choice(string.ascii_uppercase)
        y = ''.join((random.choice(string.ascii_lowercase) for _ in range(random.randint(3, 8))))
        return x + y

class LastName:

    access = ['user_modify']

    def random_(seed_):
        # random.seed(seed_)
        x = random.choice(string.ascii_uppercase)
        y = ''.join((random.choice(string.ascii_lowercase) for _ in range(random.randint(8, 12))))
        return x + y

class Birthday:

    access = ['user_modify', 'matcha_cmp']
    age_nb = range(18, 100)

    def check_age(iage):
        f = [str(n) for n in range(18, 100)]
        return iage in f

    def check(x):
        x = x.split('/')
        if len(x) != 3:
            return False
        day, month, year = x
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            return False
        # check with age

    def cmp_(b1, b2):
        year1 = b1.split('/')[-1]
        year2 = b2.split('/')[-1]
        return abs(year1 - year2) <= 5

    def random_(seed_):
        # random.seed(seed_)
        day = random.randint(1, 28)
        month = random.randint(1, 12)
        year = random.randint(1955, 2000)
        return f'{day}/{month}/{year}'


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

    
    def random_(seed_):
        # random.seed(seed_)
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


class Email:
    access = ['user_modify']

    smtp = ('@hotmail', '@outlook', '@gmail')
    smpt_ext = ('.com', '.fr')
    email_tags = (f'{_smtp}{_ext}' for _smtp in smtp for _ext in smpt_ext)

    def random_(seed_):
        # random.seed(seed_)
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



class Pwd:

    access = ['user_modify']
    pwd_len = range(8, 64)
    pwd_str = (string.ascii_lowercase, string.ascii_uppercase, string.punctuation, string.digits)

    def random_(seed_):
        # random.seed(seed_)
        punctuation = '!#$%&()*+,-./:;<=>?@[\]^_{|}~'
        all_ = string.ascii_letters + punctuation + string.digits
        rpwd = ''.join((random.choice(all_) for _ in range(random.randint(8, 64))))
        return rpwd

    def check(ipwd):
        l = (string.ascii_lowercase, string.ascii_uppercase, string.punctuation, string.digits)
        for il in l:
            if len((ch for ch in ipwd if il)) == 0:  # at least one of set
                return False
        if len(ipwd) not in range(8, 64):
            return False

class SexOrientation:

    access = ['user_modify', 'matcha_cmp']

    def random_(seed_):
        # random.seed(seed_)
        x = ('male', 'female', 'male female')
        return random.choice(x)

    def cmp(pref1, gender1, pref2, gender2):
        return gender1 in pref2 and gender2 in pref1

class Location:

    access = ['user_modify', 'matcha_cmp']

    def random_(seed_):
        # random.seed(seed_)
        locs = ('USA', 'France', 'Moon', 'Spain', 'Canada', 'Turkey', 'Mexico')
        return random.choice(locs)
        # pip install flask-simple-geoip

    def cmp_(v1, v2):
        return v1 == v2

class Tags:

    access = ['user_modify', 'matcha_cmp']

    def random_(seed_):
        # random.seed(seed_)
        tags = ('sports', 'dancing', 'art', 'movies', 'coding', 'law', 'animals', 'games', 'building', 'photograph')
        rnb = random.randint(0, len(tags))
        return tuple(random.choice(tags) for i in range(rnb))

    def cmp_(v1, v2):
        return len(set(v1) & set(v2)) > 0  # intersection keep all eq


class Gender:

    access = ['user_modify']

    def random_(seed_):
        # random.seed(seed_)
        x = ('male', 'female')
        return random.choice(x)

class Intro:

    def random_(seed_):
        # random.seed(seed_)
        nb_words = random.randint(0, 20)
        intro = ''
        for i in range(nb_words):
            len_word = random.randint(0, 10)
            word = ''.join((random.choice(string.ascii_lowercase) for _ in range(len_word)))
            intro += f' {word} '
        return intro

class Msgs:

    access = ['user_modify']

    def random_(emails, seed_):
        # random.seed(seed_)
        rnb = random.randint(0, len(emails))
        msgs = []
        for _ in range(rnb):
            msg = dict()
            msg['date'] = Timestamp.random_(seed_ + 5)
            msg['to_email'] = random.choice(emails)  # can send to himself
            msg['msg'] = Intro.random_(seed_ + 10)
            msgs.append(msg)
        return msgs

class Likes:

    access = ['user_modify']

    def random_(emails, seed_):
        # random.seed(seed_)
        rnb = random.randint(0, len(emails))
        return [random.choice(emails) for i in range(rnb)]

class Activated:

    access = ''

    def random_(seed_):
        # random.seed(seed_)
        return random.choice([True, False])

class Blocked:

    access = ''

    def random_(seed_):
        # random.seed(seed_)
        return random.choice([True, False])


def get_field_fns(which):
    clss = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    return {clsname: clsobj.__dict__[which] for clsname, clsobj in clss if which in clsobj.__dict__}

    """
    if which == 'cmp':
        return {clsname:clsobj.cmp_ for clsname,clsobj in clss}
    if which == 'random':
        return {clsname: clsobj.random_ for clsname, clsobj in clss}
    if which == 'check':
        return {clsname: clsobj.cmp_ for clsname, clsobj in clss}
    """