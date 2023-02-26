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
    activatedDevicesList = []
    
    def __init__(self, nodes, lifespan, tfMax, epochs = 0):
        self.nodes = nodes
        self.nb_nodes = len(self.nodes)
        self.lifespan = lifespan
        self.tfMax = tfMax
        self.epochs = epochs
    

    def __str__(self):
        print("List of Devices in the Simulation : ")
        for device in self.nodes:
            print(device)
        return "EOL"
    
    def predictDevices(self):
        for device in self.nodes:
            device.predict()
            #print(str(device) + ' probability P is ' + str(device.probaP))

    def activateDevices(self, monitor):
        for device in self.nodes:
            if not device.isActive:
                self.activatedDevicesList.append(device.transmit("Aloha !", monitor))
                device.isActive = True
            
        self.activatedDevicesList = [device for device in self.activatedDevicesList if device != 0]
        

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
        print("___### Start of SIMULATION ###___")

    def status(self):
        #status is called every main loop iteration (=every epoch)
        #making sure transmission duration = TF for transmitting devices
        listOfDeviceToRemove = []
        for device in self.activatedDevicesList:
            if device['self'].isActive:
                device['self'].epoch += 1
            if device['self'].epoch >= (self.tfMax):
                device['self'].standDown()
                listOfDeviceToRemove.append(device)
                                        
        self.removeDevice(listOfDeviceToRemove)


                
                
        return "ELOCH ELAPSED : {}".format(self.epochs)

    def removeDevice(self, devicesToRemove):
        for device in devicesToRemove:
            self.activatedDevicesList.remove(device)
                
    def end(self):
        self.isRunning = False
        print("___### End of SIMULATION ###___")
        
        
