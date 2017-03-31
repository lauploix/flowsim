'''
Created on Apr 26, 2016

@author: plume
'''
import unittest
from flowsim import TimedBroker
from flowsim import FlowMessage

from datetime import datetime

DATES_MIN=[datetime(year=1980, 
                month=1, 
                day=23, 
                hour=11, 
                minute=m) for m in xrange(0, 10)]

class Instanciationtests(unittest.TestCase):
    def test_instanciation(self):
        """Instantiates the classes"""
        TimedBroker()
        FlowMessage(datetime.now())
    
        
class TestFlowMessages(unittest.TestCase):
    def test_message_properties(self):
        """One can set and read properties"""
        message = FlowMessage(DATES_MIN[0])


        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()