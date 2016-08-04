'''
Created on May 12, 2016

@author: plume
'''

from flowsim import FlowMessageDeliveryException
from datetime import timedelta

class FlowAgent(object):
    """Base class for agents that can emit and receive messages from to and from the TimedBroker
    The general idea is that an agent can accept of reject messages (can_receive will check that)
    do something with it and then send 0 to N messages to the broker.
    Messages are timed. That means that an Agent will send messages at a certain time, and the agent 
    maintains the time it is available to receive a new message.
    This is simulated time, not real one.
    """ 
    def __init__(self, when, broker):
        self.when=when # The date when the agent is available to proceed with a new message
        self.broker=broker
        self.last_message=None
        
    def deliver(self, message): 
        """The method which is called when the agent gets a message delivered from the TimedBroker.
        When sent, the agent and the message are already at the right time"""
        self.last_message=message
        if not self.can_receive(message):
            raise FlowMessageDeliveryException("Agent does not accept the message")
        self._deliver(message)
        
    def _deliver(self, message): 
        """The internal implementation for delivering messages
        Agents do not need to implement super() of deliver by default.
        Most agents to NOT need to re-implement it. Only collect_messages.
        The contract is to send messages back to the broker out of the 
        input message; and to update the agent current date ("when")
        """
        messages = self._collect_messages(message)
        if messages != []:
            self.when=max([m.when for m in messages])
        for m in messages: self.broker.post_message(message)
        
    def _collect_messages(self, message):
        """returns the collection of messages to send to the broker.
        Most agents only need to implement this method to define
        the behavior when it comes to messages that get sent back
        to the broker."""
        return []
    
    def can_receive(self, message): return False #default
    
class AcceptingAgent (FlowAgent):
    def __init__(self, when, broker=None):
        super(AcceptingAgent, self).__init__(when, broker)
    
    def can_receive(self, message):
        return True
    
class EchoAgent (AcceptingAgent):
    def __init__(self, when, broker=None, delta=timedelta()):
        super(EchoAgent, self).__init__(when, broker)
        self.delta=delta
    
    def _collect_messages(self, message): 
        """The method which is called when the agent gets a message delivered from the TimedBroker.
        When sent, the agent and the message are already at the right time"""
        message.when = message.when+self.delta
        return [message]
            
class AllPropertiesMatchingAgent(FlowAgent):
    """An agent that can receive messages if the properties are equal"""
    def __init__(self, when, broker, properties={}):
        super(AllPropertiesMatchingAgent, self).__init__(when, broker)
        self.properties=properties
    def can_receive(self, message):
        return self.properties == message.properties
        
class AllMessagePropertiesMatchingAgent(FlowAgent):
    """An agent that will accept all messages if the message properties match
    the ones of the agent (message properties are a subset of the agent ones)"""
    def __init__(self, when, broker, properties={}):
        super(AllMessagePropertiesMatchingAgent, self).__init__(when, broker)
        self.properties=properties
        
    def can_receive(self, message):
        for key, value in message.properties.iteritems():
            if not (key in self.properties and self.properties[key] == value):
                return False
        return True
        
