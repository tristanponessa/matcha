import os
import time

def if_file_del(file):
    if os.path.exists(file):
        os.remove(file)
        time.sleep(1)