import random

class Simulation():
    '''
    Simulating an ALOHA Network. Each node tries to send into a single channel.
    Message is generated with probability q (active node) 
    and sent into channel with probability p.

    Collision appears if more than one node tries to communicate,
    otherwise, transmission is a success.
    '''

    def __init__(self, nodes, epochs):
        self.nodes = nodes
        self.epochs = epochs
    "L'école de la débrouille"