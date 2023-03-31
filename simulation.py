class Simulation():
    '''
    Simulating an ALOHA Network. Each node tries to send into a single channel.
    Message is generated with probability q (active node) 
    and sent into channel with probability p.

    Collision appears if more than one node tries to communicate,
    otherwise, transmission is a success.
    
    Attributes:
        - [int] nodes = number of nodes in the network
        - [int] lifespan = number of iteration in the simulation 
        - [int] tf = maximum duration of a transmission
        - [int] epochs = UNIVERSAL epoch for simulation 
        
        - [bool] isRunning = Flag for state of simulation = False (default)
        - [array] activatedDevicesList = List of devices that are currently transmitting = [] (default)
    '''

    isRunning = False
    activatedDevicesList = []
    
    def __init__(self, nodes, lifespan, tf, epochs = 0):
        self.nodes = nodes
        self.nb_nodes = len(self.nodes)
        self.lifespan = lifespan
        self.tf = tf
        self.epochs = epochs
    
    # special function for displaying a list of devices in the simulation
    def __str__(self):
        print("List of Devices in the Simulation : ")
        for device in self.nodes:
            print(device)
        return "EOL"
    
    '''
    Function to generate probabilities of transmitting over all devices in the Network
    
    param : None 
    return : None
    '''
    def predictDevices(self, SIM_WAITING_TIME):
        for device in self.nodes:
            device.predict(SIM_WAITING_TIME)
            
    '''
    Function that makes each device listen to the network, so as later that it sends its information only if no other device is communicating
    
    param : None
    return : None
    '''
    def oneDeviceIsAlreadyCommunicating(self):
        for device in self.nodes:
            if device.isActive:
                return True
        return False

    '''
    Function to proceed to transmitting pool over all devices in the Network 
    Devices have to be inactive (!device.isActive) and can either transmit or not transmit
    results are then appended to activatedDevicesList and filtered if they are NULL(0)
    
    param :[Monitor] monitor 
    return : None
    '''
    def activateDevices(self, monitor, SIM_WAITING_TIME):
        if self.oneDeviceIsAlreadyCommunicating():
            return
        else :
            for device in self.nodes:
                if not device.isActive:
                    #adding t_debut to comms history
                    device.comms_history.append([self.epochs])
                    
                    self.activatedDevicesList.append(device.transmit("Aloha !", monitor, SIM_WAITING_TIME))
                
            self.activatedDevicesList = [device for device in self.activatedDevicesList if device != 0]
        
    '''
    Function to check if simulation has to be ended
    
    param : None 
    return : [bool] True if simulation has to be ended, false if not
    '''
    def isEnd(self):
        if self.epochs==self.lifespan:
            return True
        return False 

    '''
    Function start a simulation (self.isRunning is switched to True)
    
    param : None 
    return : None
    '''
    def start(self):
        self.isRunning=True
        print("___### Start of SIMULATION ###___")

    '''
    Status function of the simulation : this function is called at every epoch of the simulation 
    it makes sure that transmission duration for each device in the Network does not exceed TF value
    
    this function increments local epoch of every activated device and checks if this local epoch exceeded TF value
    if it exceeded TF value, device is shut down and added to the list of device to remove (then removed by self.removeDevice() function)
    
    param : None 
    return : [string] number of epoch elapsed
    '''
    def status(self):
        #status is called every main loop iteration (=every epoch)
        #making sure transmission duration = TF for transmitting devices
        listOfDeviceToRemove = []
        
        for device in self.nodes:
            device.state += 1
            
        for device in self.activatedDevicesList:
            if device['self'].isActive:
                device['self'].epoch += 1
                
            if device['self'].epoch >= (self.tf):
                #adding t_fin to comms history
                device['self'].comms_history[-1].append(self.epochs)
                
                device['self'].standDown()
                listOfDeviceToRemove.append(device)

        self.removeDevice(listOfDeviceToRemove)
        #print(self.activatedDevicesList)
        
        return "EPOCH {}".format(self.epochs)

    
    '''
    Function removeDevice to remove a device from the list of activated devices in the Network
    
    param : [array] devicesToRemove
    return : None
    '''
    def removeDevice(self, devicesToRemove):
        for device in devicesToRemove:
            self.activatedDevicesList.remove(device)
             
    '''
    Function to stop the simulation (switching isRunning to False)
    
    param : None
    return : None
    '''   
    def end(self):
        self.isRunning = False
        print("___### End of SIMULATION ###___")
        
