class Monitor():
    '''
    Class Monitor for Simulating a central monitor in the Network
    
    Attributes:
        - [int] id = ID of the device = 42 (default)
        - [array] db = database of transmission received by the monitor = [] (default)
    '''
    def __init__(self, id = 42, db = []):
        self.id = id
        self.db = db
    '''
    Function receive for receiving a package 
    
    param : [dict] package 
    return : [dict] reiceived package
    '''
    def receive(self, package):
        print (">> Monitor id " + str(self.id) + " Received one package")
        self.db.append(package)
        return package