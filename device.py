import random 
from Aloha import Aloha 

class Device(Aloha):
    '''
    Class Device for Simulating a device in the Network
    
    Attributes:
        - [int] id = ID of the device
        - [float] probaP = probability of the device for sending a package
        - [bool] isActive = Is the device sending a package or not
        - [int] epoch = LOCAL epoch for the device used to track how many epochs elapsed after device started his transmission
    '''

    def __init__(self, id, w_e, theta_e, lambda_e, p_e, isActive = False, epoch = 0):
        self.id = id
        self.w_e = w_e
        self.theta_e = theta_e
        self.lambda_e = lambda_e
        self.p_e = p_e
        self.isActive = isActive
        self.epoch = epoch
        self.probaP = 0
        self.lambda_e_iterSuivante = self.lambda_e
        self.comms_history = []


    
    # special function for displaying a device information 
    def __str__(self):
        template = "Device id : {}"
        return template.format(self.id)
    
    '''
    function for predicting the probability of a device to transmit
    
    Param : None
    return : None
    '''
    def predict(self):
        self.probaP = random.random()

    '''
    function for transmitting the information based on probabilities 
    
    Param :[_] information, [Monitor] target
    return : [dict] package information if transmission occured, [bool] 0 if transmission didnt occur
    '''
    def transmit(self, information, target):
        if (random.random() < self.p_e): 
            self.isActive = True
            return target.receive(self.package(self.id, information))
        else:
            return 0
    '''
    function for package construction
    
    Param : [int]id, [_] payload
    return : [dict] dictionnary with device id and object
    '''
    def package(self, id, payload):
        return {'id': id, 'self': self}
    
    '''
    function for shutting down a device's transmission -> Device is not active anymore and epoch are reinitialized to 0
    
    Param : None
    return : None
    '''
    def standDown(self):
        self.isActive = False
        self.epoch = 0
    
