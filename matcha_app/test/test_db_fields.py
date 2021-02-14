import sys, os
print(sys.path)
print(os.getcwd())

sys.path.append('/home/user/Documents/coding/matcha') #top level, this path represents '.'



#db already imported fields,filepaths
import matcha_app.db as D


###############MAIN##############################3

if __name__ == '__main__':


    #1. load random in db
    sys.argv += ['1'] * 20
    if sys.argv[1] == '1':
        D.init_db('sqlite')
        D.load_db('sqlite', 'fake')

        #GET ALL TEST
        ps = D.db_exec('SELECT * FROM users')



        #print(ps['profile'][''])
        #print(ps)

        # SUBDCT TEST
        non_exist_subdct = {"location": "space"}
        found_subdct = {"tags": ["C++", "power"], "intro": "im a GOD"}

        ps1 = D.get_profiles(found_subdct)
        ps2 = D.get_profiles(non_exist_subdct)

        print(ps1)
        print(ps2)



        """
        D.init_db('sqlite')
        D.load_db('sqlite', 'random')
        ps = D.db_exec('SELECT * FROM users')
        D.db_exec('SELECT * FROM users')
        """

        #import json
        #x = json.load(open('./matcha_app/db_files/fake_db.json', 'r'))
        #print(len(ps))
        #ps = D.create_profiles(0)
        #print(ps)
        #for p in ps:
        #print(*x, sep='\n')
        #D.print_profile(p['profile'])
        #D.stock_profiles(ps)
        #fakeps = json.load(file_paths.fakedb)



