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
        if len(commsHistory) <= 1:
            return (self.lifespan+1)/2
        sumCommsAoI = 0
        for i in range(len(commsHistory)-1):
            AoI = 0
            for t in range(commsHistory[i], commsHistory[i+1]):
                sumCommsAoI += AoI
                AoI += 1
            
        return sumCommsAoI/(commsHistory[-1] - commsHistory[0])
    
    '''
    Function returning the maximum value of the AoI of a device
    '''
    def returnMaxAoIOfADevice(self, commsHistory):
        # Uses only the comms_history when each communication is written with the beginning epoch ONLY
        if len(commsHistory) == 0:
            return self.lifespan
        maxCommsAoI = 0
        for i in range(len(commsHistory)-1):
            if maxCommsAoI < commsHistory[i+1] - commsHistory[i]:
                maxCommsAoI = commsHistory[i+1] - commsHistory[i]
        return maxCommsAoI
    
    '''
    Function returning the minimum value of the AoI of a device
    '''
    def returnMinAoIOfADevice(self, commsHistory):
        # Uses only the comms_history when each communication is written with the beginning epoch ONLY
        if len(commsHistory) == 0:
            return self.lifespan
        minCommsAoI = self.lifespan
        for i in range(len(commsHistory)-1):
            if minCommsAoI > commsHistory[i+1] - commsHistory[i]:
                minCommsAoI = commsHistory[i+1] - commsHistory[i]
        return minCommsAoI
    
    def returnMoyAoIGlobal(self):
        moyAoI = 0
        for i in range(len(self.devicesList)):
            moyAoiDev = self.returnMoyAoIOfADevice(self.devicesList[i].comms_history)
            moyAoI += moyAoiDev
        return moyAoI/len(self.devicesList)
    
    '''
    Function printing the results of the simulation
    '''
    def printResultsAoI(self):
        print("___### Results of SIMULATION ###___")
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
        print("Average of the AoI: ", moyAoI/len(self.devicesList))
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
        axs[-1].set(xlim = (0, self.lifespan))
        for i in range(nbDevicesToDisplay):
            plt.setp(axs[i], ylabel='AoI (in epochs)')

        plt.savefig("AOI_graph.jpg")
