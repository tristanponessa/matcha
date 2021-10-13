
dbsdir = './matcha_app/db_files'

dblivetxt = f'./{dbsdir}/db_live.txt'
fakedb = f'./{dbsdir}/fake_db.json'
sqlitefile = f'./{dbsdir}/matcha.db'

generallog = './matcha_app/logs/log.txt'

import os
import time
from pathlib import Path

def if_file_del(file):
    if os.path.exists(file):
        os.remove(file)
        time.sleep(1)

#pycharm debugger calls it an error
def create_file(file):
    with open(file, 'w+'):
        pass
    time.sleep(1)

def write_file(lines : list, file):
    with open(file, 'w+') as f:
        f.writelines(lines)


#def create_file(p):
#    Path(p).touch()
