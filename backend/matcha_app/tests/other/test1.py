import random
import string 

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
        return ''.join([Random.rand(lst) for _ in range(0, rlen)])

class FirstName:
    access = ['user_modify']

    def random_():
        first = Random.rand(string.ascii_uppercase)
        rest = Random.rand_str(string.ascii_lowercase, 3, 8)
        return first + rest


def r2():  # do not assign to rand list
        
        day = Random.rand(range(1, 28))
        month = Random.rand(range(1, 12))
        year = Random.rand(range(2001, 2020))
        hour = Random.rand(range(0, 23))
        min_ = Random.rand(range(0, 59))
        sec = Random.rand(range(0, 59))
        return f'{year}-{month:02d}-{day:02d} {hour:02d}:{min_:02d}:{sec:02d}'


print(r2())
print(r2())
print(r2())
print(r2())
print(r2())
print(r2())
print(r2())

print(*[r2() for i in range(20)], sep='\n')