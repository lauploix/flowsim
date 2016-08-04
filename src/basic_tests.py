'''
Created on Apr 26, 2016

@author: plume
'''
import unittest
from flowsim import TimedBroker
from flowsim import FlowMessage
from flowsim import FlowAgent, AllPropertiesMatchingAgent, AllMessagePropertiesMatchingAgent, AcceptingAgent
from flowsim import FlowMessageDeliveryException

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
        FlowMessageDeliveryException()

    
        
class TestFlowMessages(unittest.TestCase):
    def test_message_properties(self):
        """One can set and read properties"""
        message = FlowMessage(DATES_MIN[0])
        message.properties["bla"]="bli"
        self.assertEquals("bli", message.properties["bla"])

class TestAgents(unittest.TestCase):
    def test_agent_does_not_match_random_message(self):
        """A normal agent does not accept a message by default and sends an alert if sent to anyway"""
        message = FlowMessage(DATES_MIN[1])
        agent=FlowAgent(None, None)
        self.assertFalse (agent.can_receive(message))
        self.assertRaises(FlowMessageDeliveryException, agent.deliver, message) 
        
    def test_all_properties_matching_agent_accepting_conditions(self):
        message_good = FlowMessage(DATES_MIN[1], properties={"a":1, "b":"abc"})
        message_wrong = FlowMessage(DATES_MIN[1], properties={"a":1, "b":"abcd"})
        message_bad_missing  = FlowMessage(DATES_MIN[1], properties={"a":1 })
        message_bad_too_many  = FlowMessage(DATES_MIN[1], properties={"a":1, "b":"abc", "c":2})
        agent=AllPropertiesMatchingAgent(None, None, {"a":1, "b":"abc"})
        self.assertTrue(agent.can_receive(message_good))
        self.assertFalse(agent.can_receive(message_bad_missing))
        self.assertFalse(agent.can_receive(message_bad_too_many))
        self.assertFalse(agent.can_receive(message_wrong))
        
    def test_all_message_properties_matching_agent_accepting_conditions(self):
        message_good = FlowMessage(DATES_MIN[1], properties={"a":1, "b":"abc"})
        message_wrong = FlowMessage(DATES_MIN[1], properties={"a":1, "b":"abcd"})
        message_good_missing  = FlowMessage(DATES_MIN[1], properties={"a":1 })
        message_bad_too_many  = FlowMessage(DATES_MIN[1], properties={"a":1, "b":"abc", "c":2})
        agent=AllMessagePropertiesMatchingAgent(None, None, {"a":1, "b":"abc"})
        self.assertTrue(agent.can_receive(message_good))
        self.assertTrue(agent.can_receive(message_good_missing))
        self.assertFalse(agent.can_receive(message_bad_too_many))
        self.assertFalse(agent.can_receive(message_wrong))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()