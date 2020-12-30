import sys

from gen_random import *
from sqlite_db import *
from dict_ops import *

from rand_accounts import *

def main(argv):

    master_seed = 0 if len(argv) != 2 else int(argv[1])
    conn,cur = None,None
    try:
        conn, cur = db_conn()
        init_db(conn, cur)
        profiles = gen_random_profiles(master_seed)
        #load_profiles_in_db(profiles, cur)

        #fetch tests

    
    except Exception as e:
        print(repr(e))
    finally:
        db_close(conn, cur)



if __name__ == '__main__':
    main(sys.argv)