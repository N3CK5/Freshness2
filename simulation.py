import random


class Simulation():
    '''
    Simulating an ALOHA Network. Each node tries to send into a single channel.
    Message is generated with probability q (active node) 
    and sent into channel with probability p.

    Collision appears if more than one node tries to communicate,
    otherwise, transmission is a success.
    '''

    isRunning = False
    tfValue = 0

    def __init__(self, nodes, lifespan, tfMax, epochs = 0):
        self.nodes = nodes
<<<<<<< HEAD
        self.nb_nodes = len(self.nodes)
        self.lifespan = lifespan
        self.tfMax = tfMax
        self.epochs = epochs
    

    def __str__(self):
        print("List of Devices in the Simulation : ")
        for device in self.nodes:
            print(device)
        return "EOL"
    
    def isTF(self):
        if self.tfValue==self.tfMax:
            self.tfValue = 0
            return True
        return False

    def isEnd(self):
        if self.epochs==self.lifespan:
            return True
        return False 

    def start(self):
        self.isRunning=True
        print("### Start of SIMULATION ###")

    def status(self):
        print("EPOCH ", self.epochs)

    def end(self):
        self.isRunning = False
        print("### End of SIMULATION ###")
        
