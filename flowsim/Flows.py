'''
Created on Apr 26, 2016

@author: plume
'''

from datetime import timedelta

class Orchestrator(object):
    def __init__(self, broker):
        self.broker = broker
        
    def play(self):
        first_message = self.broker.messages[0]
        for agent in self.broker.agents_before(first_message.when):
            agent.when = first_message.when
            

class TimedBroker(object):
    def __init__(self):
        self.messages = [] 
        self.agents=[]

    def add_agent(self, agent):
        self.agents.append(agent)
        self.agents.sort(key=lambda x: x.when)
        
    def post_message(self, message):
        self.messages.append(message)
        self.messages.sort(key=lambda x: x.when)
                
    def messages_before(self, date):
        for message in self.messages:
            if message.when <= date: 
                yield message
            else:
                raise StopIteration() # Messages are ordered
    
    def agents_before(self, date):
        for agent in self.agents:
            if agent.when <= date: 
                yield agent
            else:
                raise StopIteration() # Messages are ordered