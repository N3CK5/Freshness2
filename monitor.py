class Monitor():
    
    def __init__(self, id = 42, db = []):
        self.id = id
        self.db = db

    def receive(self, package):
        print (">> Monitor id " + str(self.id) + " Received one package")
        self.db.append(package)
        return package