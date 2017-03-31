'''
Created on May 12, 2016

@author: plume
'''

class FlowMessage(object):
    """base class for all messages
    Messages have properties.
    They are delivered to agents by the TimedBroker
    Messages are also created by agents and sent to the TimeBroker for further delivery""" 
    def __init__(self, when, properties={}):
        self.when=when # The date when the message is available to retrieve

