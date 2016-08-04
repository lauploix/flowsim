'''
Created on Apr 26, 2016

@author: plume
'''
import unittest
from flowsim import TimedBroker
from flowsim import FlowMessage
from flowsim import AcceptingAgent

from datetime import datetime

# Dates are 1 minute apart from each other
DATES_MIN=[datetime(year=1980, 
                month=1, 
                day=23, 
                hour=11, 
                minute=m) for m in xrange(0, 3)]

class TestBasicDistributionTimeBrokerMessages(unittest.TestCase):
    
    def setUp(self):
        self.broker=TimedBroker()
        
    def test_push_and_read_simple_message(self):
        """Posting a message in the broker makes it available in the broker"""
        d=DATES_MIN[0]
        input_mes =FlowMessage(d)
        self.broker.post_message(input_mes)
        output_mes=self.broker.messages[0]
        self.assertEquals(input_mes, output_mes)

    def test_pushed_messages_in_time_order_popped_back_in_oder(self):
        """Posting 2 messages with ordered availability dates time 
        makes it available in the broker in that same order"""
        dates = DATES_MIN[0:2]
        input_messages = [FlowMessage(d) for d in dates]
        for mes in input_messages: self.broker.post_message(mes)
        output_messages = [self.broker.messages[i] for i in xrange(2)]
        self.assertEquals(output_messages[0].when, DATES_MIN[0])
        self.assertEquals(output_messages[1].when, DATES_MIN[1]) 

    def test_pushed_messages_in_reverse_time_popped_back_in_oder(self):
        """Posting 2 messages with reverse availability dates time 
        makes it available in the broker in that same order"""
        dates = DATES_MIN[0:2][::-1]
        input_messages = [FlowMessage(d) for d in dates]
        for mes in input_messages: self.broker.post_message(mes)
        output_messages = [self.broker.messages[i] for i in xrange(2)]
        self.assertEquals(output_messages[0].when, DATES_MIN[0])
        self.assertEquals(output_messages[1].when, DATES_MIN[1])
        
    def test_push_message_to_agent_with_message_ready_before_agent(self):
        """Posting a message and having it delivered to an agent
        with availability date of message being before availability of agent
        makes broker jump to agent date"""
        self.broker.post_message(FlowMessage(DATES_MIN[0]))
        agent= AcceptingAgent(DATES_MIN[1])
        self.broker.add_agent(agent)
        self.broker.distribute_next()
        self.assertEquals(self.broker.when, DATES_MIN[1])
        self.assertEquals(agent.when, DATES_MIN[1])
        self.assertEquals(agent.last_message.when, DATES_MIN[1])
                
    def test_push_message_to_agent_with_agent_ready_before_message(self):
        """Posting a message and having it delivered to an agent
        with availability date of message being before availability of agent
        makes broker jump to message date"""
        message=FlowMessage(DATES_MIN[1])
        self.broker.post_message(message)
        agent= AcceptingAgent(DATES_MIN[0])
        self.broker.add_agent(agent)
        self.broker.distribute_next()
        self.assertEquals(self.broker.when, DATES_MIN[1])
        self.assertEquals(agent.when, DATES_MIN[1])
        self.assertEquals(message.when, DATES_MIN[1])
        
    def test_message_sent_to_agent(self):
        """A message, when sent to an agent, makes it received by agent and gone from broker"""
        message = FlowMessage(DATES_MIN[1])
        self.broker.post_message(message)
        agent= AcceptingAgent(DATES_MIN[0])
        self.broker.add_agent(agent)
        self.broker.distribute_next()
        # The last message we have in the agent is the one that got delivered to the broker
        self.assertEquals(message, agent.last_message)
        # There is no message anymore in the broker 
        self.assertEquals([], self.broker.messages)
                        
    def test_message_sent_to_first_agent_in_order(self):
        """A message, when sent to the first agent available, agents added in right order and message before"""
        message = FlowMessage(DATES_MIN[0])
        agent_1= AcceptingAgent(DATES_MIN[1])
        agent_2= AcceptingAgent(DATES_MIN[2])
        self.broker.add_agent(agent_1)
        self.broker.add_agent(agent_2)
        self.broker.post_message(message)
        self.broker.distribute_next()
        # agent 1 got the message
        self.assertEquals(message, agent_1.last_message)
        #agent 2 got no message
        self.assertEquals(None, agent_2.last_message)
        # There is no message anymore in the broker 
        self.assertEquals([], self.broker.messages)
        
        #Message and agent now at the same time
        self.assertEquals(agent_1.when, message.when)
        # The date is the one of the agent, because the agent came after
        self.assertEquals(agent_1.when, DATES_MIN[1])
        
    def test_2_messages_sent_to_agent_in_order(self):
        """If 2 messages are sent, the first message is sent first if both can be accepted"""
        message_1 = FlowMessage(DATES_MIN[0])
        message_2 = FlowMessage(DATES_MIN[1])
        agent= AcceptingAgent(DATES_MIN[2])
        self.broker.add_agent(agent)
        self.broker.post_message(message_1)
        self.broker.post_message(message_2)
        self.broker.distribute_next()
        # agent got the first message
        self.assertEquals(message_1, agent.last_message)
        # There is no message anymore in the broker 
        self.assertEquals([message_2], self.broker.messages)
        #Message and agent now at the same time
        self.assertEquals(agent.when, message_1.when)
        self.assertEquals(agent.when, DATES_MIN[2])
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()