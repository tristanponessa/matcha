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

def gen_random_firstname(seed_):
    random.seed(seed_)
    x = random.choice(string.ascii_upper)
    ''.join(random.choice(string.ascii_) for _ in range(random.randint(8,64)))
    

def gen_random_lastname(seed_):
    random.seed(seed_)

def gen_random_profilepic(seed_):
    random.seed(seed_)
    #choose 1 of all pics

def gen_random_pics(seed_):
    random.seed(seed_)
    #choose random nb 0-3


def gen_random_email(seed_):
    random.seed(seed_)
    r = random.choice

    user_set = string.ascii_letters + '_'
    smtp = ('@hotmail', '@outlook', '@gmail')
    ext = ('.com', '.fr')

    rid = ''.join(r(user_set) for _ in range(random.randint(1,25)))
    rand_email = rf'{rid}{r(smtp)}{r(ext)}'

    return rand_email

def gen_random_pwd(seed_):
    random.seed(seed_)
    all_ = string.ascii_letters + string.punctuation + string.digits
    rpwd = ''.join(random.choice(all_) for _ in range(random.randint(8,64)))
    return rpwd

def gen_random_birthdate(seed_):
    random.seed(seed_)
    day = random.randint(1,28)
    month = random.randint(1,12)
    year = random.randint(1955,2000)
    return f'{day}/{month}/{year}'

def get_random_sexori(seed_):
    random.seed(seed_)
    x = ('straight', 'gay', 'bio')
    return random.choice(x)

funs = (gen_random_email, gen_random_pwd, gen_random_birthdate, get_random_sexori)

"""
for f in funs:
    for i in range(1,20):
        a = f(i)
        b = f(i)
        print(rf'fun: {f.__name__} seed{i} : {a}')
    print('------')
"""

master_seed = 0
nb_users = 20
min_seed = (nb_users * master_seed)
max_seed = min_seed + nb_users
for seed_nb in range(min_seed,max_seed):
    print(f'profile {seed_nb}------')
    for f in funs:
        a = f(seed_nb)
        print(rf'fun: {f.__name__} seed{seed_nb} : {a}')
    



