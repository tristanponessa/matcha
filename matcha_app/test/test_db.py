import sys, os
print(sys.path)
print(os.getcwd())

sys.path.append('/home/user/Documents/coding/matcha')
sys.path.append('/home/user/Documents/coding/matcha/matcha_app')


import matcha_app


from matcha_app.fields import *
from matcha_app.db import *


###############MAIN##############################3

if __name__ == '__main__':
    #test   fields
    get_field_fns('random_')
    get_field_fns('checks')
    get_field_fns('cmp_')

    pass

    #randps = create_profiles(0)
    #fakeps = json.load(file_paths.fakedb)