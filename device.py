class Device():
    '''
    Device
    '''
    def __init__(self, id):
        self.id = id

    def __str__(self):
        template = "Device id : {}"
        return template.format(self.id)
    
    def transmit(self, information, target):
        return target.receive(package(self, self.id, information))

    def package(self, id, payload):
        return {'id': id, 'payload': payload}

    def standby(self):
        return 0
