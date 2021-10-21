import sys, os
print(sys.path)
print(os.getcwd())

sys.path.append('/home/tristanponessa/Documents/coding/matcha') #top level, this path represents '.'



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
        #ps = D.db_exec('SELECT * FROM users')
        ps = D.get_profiles('*')
        original_ps = D.get_profiles('*')
        #print(ps['profile'][''])
        #print(ps)

        print(D.get_field_fns('random_'))
        print(D.get_field_fns('check'))
        print(D.get_field_fns('cmp_'))

        print(D.cls_for_field('birthdate'))
        print(D.cls_for_field('location'))
        print(D.cls_for_field('pwd'))


        ###################### SUBDCT TEST
        #with fakedb
        non_exist_subdct = {"location": "space"}
        found_subdct = {"tags": ["C++", "power"], "intro": "im a GOD"}

        ps1 = D.get_profiles(found_subdct)
        ps2 = D.get_profiles(non_exist_subdct)
        ps3 = D.get_profiles({'blocked' : False})

        print(len(ps1)) #1
        print(len(ps2)) #must be 0
        print(len(ps3)) #must be 2
        ##################################

        ################ MATCHA TEST
        #with fake db
        all_ps = ps.copy()
        type_ = 'birthdate'
        print('nb of ps : ', len(ps))
        ps = D.sort_profiles(type_, False, ps)
        print(f'ordered by {type_}')
        for i,p in enumerate(ps):
            print(f"{i} {p[type_]} ({p['email']})")
        print('nb of ps : ', len(ps))
        ps = D.sort_profiles(type_, True, ps)
        print(f'ordered by {type_}')
        for i, p in enumerate(ps):
            print(f"{i} {p[type_]} ({p['email']})")
        print('nb of ps : ', len(ps))

        ps5 = D.filter_profiles({'location': 'Mars'}, original_ps.copy())
        print(f'ordered by ', {'location': 'Mars'})
        for i, p in enumerate(ps5):
            print(f"{i} {p['location']} ({p['email']})")
        print('nb of ps : ', len(ps5))

        ps6 = D.filter_profiles({'location': 'Mars', 'birthdate': '1995'}, original_ps.copy())
        print('filtered by ', {'location': 'Mars', 'birthdate': '1995'})
        for i, p in enumerate(ps6):
            print(f"{i} {p['location']} {p['birthdate']}  ({p['email']})")
        print('nb of ps : ', len(ps6))


        psm = D.ft_matcha(ps[0], original_ps.copy())
        for i, p in enumerate(psm):
            print(f"{i} {ps[0]['email']} <<>> ({p['email']})")



        ###############################








