import math
from matplotlib import pyplot as plt

class Results():
    '''
    Gives and prints the results
    '''
    
    def __init__(self, devicesList, lifespan):
        self.devicesList = devicesList
        self.lifespan = lifespan

    '''
    Function modifying the communication history of each device to make it simplier to be displayed
    '''
    def modifyCommsHistories(self):
        for i in range(len(self.devicesList)):
            print(self.devicesList[i].p_e)
            self.devicesList[i].comms_history = [element[0] for element in self.devicesList[i].comms_history if len(element) > 1]

        for i in range(len(self.devicesList)):
            for j in range(len(self.devicesList)):
                if i > j:
                    ensI = set(self.devicesList[i].comms_history)
                    ensJ = set(self.devicesList[j].comms_history)
                    ensI1 = ensI - ensJ
                    ensJ1 = ensJ - ensI
                    lI = list(ensI1)
                    lJ = list(ensJ1)
                    lI.sort()
                    lJ.sort()
                    self.devicesList[i].comms_history = lI
                    self.devicesList[j].comms_history = lJ
    
    '''
    Function returning the mean value of the AoI of a device
    '''
    def returnMoyAoIOfADevice(self, commsHistory):
        # Uses only the comms_history when each communication is written with the beginning epoch ONLY
        if len(commsHistory) == 0:
            return self.lifespan
        sumCommsAoI = commsHistory[0]
        j = 1
        for i in range(len(commsHistory)-1):
            sumCommsAoI += commsHistory[i+1] - commsHistory[i]
            j+=1
        sumCommsAoI += self.lifespan - commsHistory[-1]
        j+=1
        return sumCommsAoI/(len(commsHistory)+1)
    
    '''
    Function returning the maximum value of the AoI of a device
    '''
    def returnMaxAoIOfADevice(self, commsHistory):
        # Uses only the comms_history when each communication is written with the beginning epoch ONLY
        if len(commsHistory) == 0:
            return self.lifespan
        maxCommsAoI = commsHistory[0]
        for i in range(len(commsHistory)-1):
            if maxCommsAoI < commsHistory[i+1] - commsHistory[i]:
                maxCommsAoI = commsHistory[i+1] - commsHistory[i]
        maxCommsAoI = max(maxCommsAoI, self.lifespan - commsHistory[-1])
        return maxCommsAoI
    
    '''
    Function returning the minimum value of the AoI of a device
    '''
    def returnMinAoIOfADevice(self, commsHistory):
        # Uses only the comms_history when each communication is written with the beginning epoch ONLY
        if len(commsHistory) == 0:
            return self.lifespan
        minCommsAoI = commsHistory[0]
        for i in range(len(commsHistory)-1):
            if minCommsAoI > commsHistory[i+1] - commsHistory[i]:
                minCommsAoI = commsHistory[i+1] - commsHistory[i]
        minCommsAoI = min(minCommsAoI, self.lifespan - commsHistory[-1])
        return minCommsAoI
    
    '''
    Function printing the results of the simulation
    '''
    def printResultsAoI(self):
        print("Device   Moy  Max  Min")
        moyAoI = 0
        minAoI = math.inf
        maxAoI = 0
        for i in range(len(self.devicesList)):
            moyAoiDev = self.returnMoyAoIOfADevice(self.devicesList[i].comms_history)
            maxAoIDev = self.returnMaxAoIOfADevice(self.devicesList[i].comms_history)
            minAoIDev = self.returnMinAoIOfADevice(self.devicesList[i].comms_history)
            moyAoI, maxAoI, minAoI = moyAoI + moyAoiDev, max(maxAoI, maxAoIDev), min(minAoI, minAoIDev)
            # We print here the mean, min and max value of the AoI of each device then of the network
            print("Device", i, moyAoiDev, maxAoIDev, minAoIDev)
        print("Results:")
        print("Mean of the AoI: ", moyAoI/len(self.devicesList))
        print("Max of the AoI: ", maxAoI)
        print("Min of the AoI: ", minAoI)
    
    '''
    Function ploting the AoI of the devices

    param : [int] nbDevicesToDisplay : corresponds to the number of devices whose AoI must be displayed
    '''
    def plotAoIGraphs(self, nbDevicesToDisplay):
        fig, axs = plt.subplots(nbDevicesToDisplay, sharex=True, sharey=True)
        fig.suptitle("Age of Information for each device")

        X = [[] for k in range(nbDevicesToDisplay)]
        Y = [[] for k in range(nbDevicesToDisplay)]
        #colorGraphs = {0: 'g-', 1:'b-', 2:'r-',3:'c-', 4:'k-', 5:'m-'}
        colorGraphs = {0: 'g-', 1:'b-', 2:'r-',3:'c-', 4:'orange', 5:'k-', 6:'m-'}

        for k in range(nbDevicesToDisplay):
            X[k].append(0)
            Y[k].append(0)
            if len(self.devicesList[k].comms_history) == 0:
                X[k].append(self.lifespan)
                Y[k].append(self.lifespan)
                axs[k].plot(X[k], Y[k], colorGraphs[k%len(colorGraphs)])
                continue
            X[k].append(self.devicesList[k].comms_history[0])
            Y[k].append(self.devicesList[k].comms_history[0])
            i = -1
            for i in range(len(self.devicesList[k].comms_history) - 1):
                X[k].append(self.devicesList[k].comms_history[i])
                Y[k].append(0)
                X[k].append(self.devicesList[k].comms_history[i+1])
                Y[k].append(self.devicesList[k].comms_history[i+1] - self.devicesList[k].comms_history[i])
                X[k].append(self.devicesList[k].comms_history[i+1])
                Y[k].append(0)
            X[k].append(self.devicesList[k].comms_history[i+1])
            Y[k].append(0)
            X[k].append(self.lifespan)
            Y[k].append(self.lifespan - self.devicesList[k].comms_history[i+1])
            axs[k].plot(X[k], Y[k], colorGraphs[k%len(colorGraphs)])

        plt.setp(axs[-1], xlabel='Time (in epochs)')
        for i in range(nbDevicesToDisplay):
            plt.setp(axs[i], ylabel='AoI (in epochs)')

        plt.savefig("AOI_graph.jpg")