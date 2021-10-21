import sys

sys.path.append('C:/Users/trps/Documents/my_stuff/coding/matcha/backend/matcha_app/')
import fields as fields_FILE


def print_profiles(pros):
    for i,p in enumerate(pros):
        print(f'profile {i}')
        for k,v in p.items():
            if k == 'msgs':
                print(f'    msgs sent: {len(v)}')
                for msg in v:
                        print(f'        {msg}')
                print()
            elif k == 'likes':
                print(f'    likes : {len(v)}')
                for like in v:
                        print(f'        {like}')
            else:
                print(f'    {k} : {v}')
        print('\n' * 3)

if __name__ == '__main__':

    pros = fields_FILE.gen_rand_profiles(10)