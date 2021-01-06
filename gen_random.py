"""
    use r for raw strings in order to auto escape \n and others in case 
    random gens it

    there's a master seed and a classic seed
    someone who generates random accounts will give a mast.seed
    a mseed will be N->M classic s
    ms1 : seeds 0->1000
    ms2 : seeds
    user 1 has seed1 on ms1
    user 1 has seed1001 on ms2


"""

import random
import string
import os



def gen_random_firstname(seed_):
    random.seed(seed_)
    x = random.choice(string.ascii_uppercase)
    y = ''.join((random.choice(string.ascii_lowercase) for _ in range(random.randint(3,8))))
    return x + y
    

def gen_random_lastname(seed_):
    random.seed(seed_)
    x = random.choice(string.ascii_uppercase)
    y = ''.join((random.choice(string.ascii_lowercase) for _ in range(random.randint(8,12))))
    return x + y

def gen_random_profilepic(seed_):
    random.seed(seed_)
    url = './pics'
    pics = os.listdir(url)
    r = random.randint(0, len(pics) - 1)
    p = f'{url}/{pics[r]}'
    return p


    #choose 1 of all pics

def gen_random_pics(seed_):
    random.seed(seed_)
    url = './pics'
    pics = os.listdir(url)
    nb = random.randint(0,4)
    p = []
    for _ in range(nb):
        r = random.randint(0,len(pics) - 1)
        p.append(f'{url}/{pics[r]}')
    return p


def gen_random_email(seed_):
    random.seed(seed_)
    r = random.choice

    user_set = string.ascii_letters + '_'
    smtp = ('@hotmail', '@outlook', '@gmail')
    ext = ('.com', '.fr')

    rid = ''.join((r(user_set) for _ in range(random.randint(1,25))))
    rand_email = rf'{rid}{r(smtp)}{r(ext)}'

    return rand_email

def gen_random_pwd(seed_):
    random.seed(seed_)
    punctuation = '!#$%&()*+,-./:;<=>?@[\]^_{|}~'
    all_ = string.ascii_letters + punctuation + string.digits
    rpwd = ''.join((random.choice(all_) for _ in range(random.randint(8,64))))
    return rpwd

def gen_random_birthdate(seed_):
    random.seed(seed_)
    day = random.randint(1,28)
    month = random.randint(1,12)
    year = random.randint(1955,2000)
    return f'{day}/{month}/{year}'

def gen_random_date(seed_):
    random.seed(seed_)
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(2001, 2020)
    hour = random.randint(0, 23)
    min_ = random.randint(0, 59)
    sec = random.randint(0, 59)
    return f'{day}/{month}/{year} {hour}:{min_}:{sec}'


def gen_random_sexori(seed_):
    random.seed(seed_)
    x = ('straight', 'gay', 'bio')
    return random.choice(x)

def gen_random_intro(seed_):
    random.seed(seed_)
    nb_words = random.randint(0, 20)
    intro = ''
    for i in range(nb_words):
        len_word = random.randint(0, 10)
        word = ''.join((random.choice(string.ascii_lowercase) for _ in range(len_word)))
        intro += f' {word} '
    return intro


def gen_random_discussions(emails, seed_):
    random.seed(seed_)
    rnb = random.randint(0, len(emails))
    msgs = []
    for _ in range(rnb):
        msg = dict()
        msg['date'] = gen_random_date(seed_)
        msg['to_email'] = random.choice(emails) #can send to himself
        msg['msg'] = gen_random_intro(seed_)
        msgs.append(msg)
    return msgs








def gen_random_likes(emails, seed_):
    random.seed(seed_)
    rnb = random.randint(0, len(emails))
    return [random.choice(emails) for i in range(rnb)]

def gen_random_interests(seed_):
    random.seed(seed_)
    tags = ('sports', 'dancing', 'art', 'movies', 'coding', 'law', 'animals', 'games')
    rnb = random.randint(0, len(tags))
    return [random.choice(tags) for i in range(rnb)]

def gen_random_block(seed_):
    random.seed(seed_)
    return random.choice([True, False])
def gen_random_activated(seed_):
    random.seed(seed_)
    return random.choice([True, False])
def gen_random_location(seed_):
    random.seed(seed_)
    locs = ('USA', 'France', 'Moon')
    return random.choice(locs)
     #pip install flask-simple-geoip



###############INTEGRATION FUNCTIONS##########################
import inspect
import sys

#funs = (gen_random_firstname, gen_random_lastname,gen_random_profilepic, gen_random_pics, gen_random_email,
#        gen_random_pwd, gen_random_birthdate, get_random_sexori)


def get_all_random_funs():
    check_funs = {}
    cur_file_members = inspect.getmembers(sys.modules[__name__])
    for member in cur_file_members:
        member_name, member_val = member
        if member_name.startswith('get_random'):
            check_funs[member_name] = member_val
    return check_funs

"""
for f in funs:
    for i in range(1,20):
        a = f(i)
        b = f(i)
        print(rf'fun: {f.__name__} seed{i} : {a}')
    print('------')
"""



#1generate random emails
#attach rest of data to them cause some need email list

def gen_random_profiles(master_seed):
    funs = get_all_random_funs()
    profiles = [] #to put into db list of dicts

    nb_users = 20
    min_seed = (nb_users * master_seed)
    max_seed = min_seed + nb_users
    for seed_nb in range(min_seed, max_seed):
        #print(f'profile {seed_nb}------')
        profile = dict()
        for f in funs:
            a = f(seed_nb)
            #print(rf'fun: {f.__name__} seed{seed_nb} : {a}')
            profile[f.__name__] = a
        #missing rand funs
        profile['blocked'] = False
        profile['activated'] = True
        profiles.append(profile)
    return profiles


def gen_random_profiles2(master_seed):
    nb_users = 20
    min_seed = (nb_users * master_seed)
    max_seed = min_seed + nb_users

    funs = get_all_random_funs()
    seed_nbs = [s for s in range(min_seed, max_seed)]
    profiles = [] #to put into db list of dicts
    emails = [gen_random_email(seednb) for seednb in seed_nbs]



    for seed_nb in range(min_seed, max_seed):
        #print(f'profile {seed_nb}------')
        profile = dict()
        for f in funs:
            a = f(seed_nb)
            #print(rf'fun: {f.__name__} seed{seed_nb} : {a}')
            profile[f.__name__] = a
        #missing rand funs
        profile['blocked'] = False
        profile['activated'] = True
        profiles.append(profile)
    return profiles

#def fetch_profile_in_db(cur, data):
#    r = exec_sql(cur, Sql_cmds.fetch.format('users')
#    profiles = r['']

    
#gen pofile dict to put into db

