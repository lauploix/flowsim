'''
Created on Apr 26, 2016

@author: plume
'''
import unittest
from flowsim import TimedBroker
from flowsim import FlowMessage
from flowsim import EchoAgent

from datetime import datetime, timedelta

# Dates are 1 minute apart from each other
DATES_MIN=[datetime(year=1980, 
                month=1, 
                day=23, 
                hour=11, 
                minute=m) for m in xrange(0, 3)]

DELTA_10_s = timedelta(seconds=10)
DELTA_25_s = timedelta(seconds=25)


class TestComplexDistributionTimeBrokerMessages(unittest.TestCase):
    
    def setUp(self):
        self.broker=TimedBroker()
        
    def test_simple_echo(self):
        """Sending a message (dated before the agent) to an "echo" agent will make the same message come back, dated as the agent is."""
        message = FlowMessage(DATES_MIN[0])                # Message on date 0
        agent=EchoAgent(DATES_MIN[1], broker=self.broker)  # Agent  on date 1
        self.broker.add_agent(agent)
        
        self.broker.post_message(message)   
        self.broker.distribute_next()
        
        #If we post the message, it comes back in the broker. Just moved in time
        self.assertEquals(self.broker.messages, [message])
        self.assertEquals(DATES_MIN[1], message.when)
                
    def test_time_delta_agent(self):
        """Sending a message (dated before the agent) to an "echo" agent that has a delta time 
        will make the same message come back, dated as the agent is + delta time.
        The delta is here to enforce a "work" delay on the echo agent."""
        message = FlowMessage(DATES_MIN[0])
        agent=EchoAgent(DATES_MIN[1], broker=self.broker, delta=DELTA_10_s)
        self.broker.add_agent(agent)
        
        self.broker.post_message(message)
        self.broker.distribute_next()
        
        #If we post the message, it comes back in the broker. Just moved in time
        self.assertEquals(self.broker.messages, [message])
        self.assertEquals(DATES_MIN[1]+DELTA_10_s, message.when)
        self.assertEquals(agent.when, message.when)
        
    #def 
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()