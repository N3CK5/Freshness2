class Device():
    '''
    Device
    '''
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __str__(self):
        return "Device id : " + id + " type: " + type
    
    def transmit(self):
        return 0

    def standby(self):
        return 0