
dbsdir = './matcha_app/db_files'

dblivetxt = './matcha_app/db_files/db_live.txt'
fakedb = './matcha_app/db_files/fake_db.json'
sqlitefile = './matcha_app/db_files/matcha.db'

generallog = './matcha_app/logs/log.txt'

import os
import time
from pathlib import Path

def if_file_del(file):
    if os.path.exists(file):
        os.remove(file)
        time.sleep(2)

#pycharm debugger calls it an error
def create_file(file):
    with open(file, 'w+'):
        pass
    time.sleep(2)

def write_file(lines : list, file):
    with open(file, 'w+') as f:
        f.writelines(lines)


#def create_file(p):
#    Path(p).touch()
