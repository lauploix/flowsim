'''
Created on May 12, 2016

@author: plume
'''

#from flowsim import FlowMessageDeliveryException
#from datetime import timedelta

class FlowAgent(object):
    def __init__(self, when):
        self.when=when # The date when the agent is available to proceed with a new message

    def process(self):
        pass
    
    def pick_messages_from_broker(self, broker):
        pass
    
    def deliver_tp_broker(self, broker):
        pass