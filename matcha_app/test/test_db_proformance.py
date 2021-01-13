import unittest
import sys
sys.path.append("..")
from sqlite_db import *
from gen_random import *
from dict_ops import *

class TestDbProformance(unittest.TestCase):

    def test_run_manager(self):
        #db_manager()
        self.assertFalse('')


        pass


if __name__ == '__main__':
    unittest.main()