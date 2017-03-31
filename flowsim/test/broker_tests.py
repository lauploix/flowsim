'''
Created on Sep 28, 2016

@author: plume
'''
import unittest
from datetime import datetime, timedelta

DATES_MIN=[datetime(year=1980, 
                month=1, 
                day=23, 
                hour=11, 
                minute=m) for m in xrange(0, 3)]

DELTA_10_s = timedelta(seconds=10)
DELTA_25_s = timedelta(seconds=25)


class BrokerTest(unittest.TestCase):
    def test_add_agents(self):
        pass
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()