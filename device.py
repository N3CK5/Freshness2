import random 

class Device():
    '''
    Device
    '''

    def __init__(self, id, isActive = False, epoch = 0):
        self.id = id
        self.probaP = 0
        self.probaQ = 0
        self.isActive = isActive
        self.epoch = epoch
        
    def __str__(self):
        template = "Device id : {}"
        return template.format(self.id)
    
    def predict(self):
        self.probaP = random.random()
        self.probaQ = random.random()

    def transmit(self, information, target):
        if (random.random() < 0.3): 
            self.isActive = True
            return target.receive(self.package(self.id, information))
        else:
            return 0

    def package(self, id, payload):
        #return {'id': id, 'status': self.isActive, 'payload': payload, 'self': self}
        return {'id': id, 'epoch':self.epoch, 'status': self.isActive, 'self': self}

    def standDown(self):
        self.isActive = False
        self.epoch = 0
    