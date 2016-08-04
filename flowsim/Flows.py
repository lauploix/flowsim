'''
Created on Apr 26, 2016

@author: plume
'''

from datetime import timedelta

class FlowMessageDeliveryException(Exception):
    pass

class TimedBroker(object):
    def __init__(self):
        self.messages = [] 
        self.when=None
        self.agents=[]

    def post_message(self, message):
        self.messages.append(message)
        self.messages.sort(key=lambda x: x.when)
        
    def distribute_next(self):
        # Find the message and the agent to distribute to
        message = self.messages.pop(0)
        agent = self.agents[0]
        
        # The time when we deliver the message to the agent
        new_when=max ((agent.when, message.when))
        
        # Now set the time for self, agent, and delivered message
        self.when = new_when
        message.when=new_when
        agent.when=new_when
        
        # Deliver the message at the right time
        agent.deliver(message)
        
    def add_agent(self, agent):
        self.agents.append(agent)
        self.agents.sort(key=lambda x: x.when)
        
