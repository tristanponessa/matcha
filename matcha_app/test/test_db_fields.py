import sys, os
print(sys.path)
print(os.getcwd())

sys.path.append('/home/user/Documents/coding/matcha')
sys.path.append('/home/user/Documents/coding/matcha/matcha_app')
sys.path.append('/home/user/Documents/coding/matcha/matcha_app/db_files')

#jezuz christ
#sys.path.append('/home/user/Documents/coding/matcha')
#sys.path.append('/home/user/Documents/coding/matcha/matcha_app')
#sys.path.append('/home/user/Documents/coding/matcha/matcha_app/db_files')


#db already imported fields,filepaths
import matcha_app.db as D


###############MAIN##############################3

if __name__ == '__main__':

    #1. load random in db
        D.init_db('sqlite')
        #D.load_db('sqlite', 'random')
        #fakeps = json.load(file_paths.fakedb)



