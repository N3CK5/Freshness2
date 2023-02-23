import random 

class Device():
    '''
    Device
    '''
    def __init__(self, id):
        self.id = id
        self.probaP = 0
        self.probaQ = 0

    def __str__(self):
        template = "Device id : {}"
        return template.format(self.id)
    
    def predict(self):
        self.probaP = random.random()
        self.probaQ = random.random()

    def transmit(self, information, target):
        if (random.random() < self.probaP): 
            return target.receive(self.package(self.id, information))
        else:
            pass

    def package(self, id, payload):
        return {'id': id, 'payload': payload}

    def standby(self):
        return 0
