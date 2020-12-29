"""
    use r for raw strings in order to auto escape \n and others in case 
    random gens it

"""

import random
import string

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


funs = (gen_random_email, gen_random_pwd)

for f in funs:
    for i in range(18,20):
        a = f(i)
        b = f(i)
        print(rf'fun: {f.__name__} seed{i} : {a}')
    print('------')


