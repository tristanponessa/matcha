import sys, os
print(sys.path)
print(os.getcwd())

sys.path.append('/home/user/Documents/coding/matcha')
sys.path.append('/home/user/Documents/coding/matcha/matcha_app')


import matcha_app

#db already imported fields
import matcha_app.db as D


###############MAIN##############################3

if __name__ == '__main__':
    #test   fields
    print(F.get_field_fns('random_'))
    F.get_field_fns('check')
    F.get_field_fns('cmp_')

    pass

    #randps = create_profiles(0)
    #fakeps = json.load(file_paths.fakedb)