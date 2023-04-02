from device import Device
from monitor import Monitor
from simulation import Simulation
from Aloha import Aloha
from results import Results
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from celluloid import Camera

#CONSTANTS
NB_DEVICES = 295
SIM_LIFESPAN = 15*60*15
SIM_TF = 1
ITERATIONS_ALOHA = 1000
SIM_WAITING_TIME = 15*60
NB_SIMULATIONS = 1



#Display function for processing data and displaying it with matplotlib
def display(activatedDevicesList, camera):
    
    for device in activatedDevicesList:
        if len(activatedDevicesList) > 1:
            rectangle = Rectangle((sim.epochs, device['id'] - 1), 1, 1, edgecolor = 'None', facecolor='red', lw = 1)
        else :
            rectangle = Rectangle((sim.epochs, device['id'] - 1), 1, 1, edgecolor = 'None', facecolor='green', lw = 1)
        listOfPatches.append([device['id'],rectangle])
    
    for patch in listOfPatches:
        ax.add_patch(patch[1])
        rx, ry = patch[1].get_xy()
        cx = rx + patch[1].get_width()/2.0
        cy = ry + patch[1].get_height()/2.0
        #ax.annotate('{}'.format(patch[0]), (cx, cy), color='black', weight='bold', fontsize=6, ha='center', va='center')
    
    plt.xticks([i*10 for i in range(SIM_LIFESPAN//10+1)], [i*10 for i in range(SIM_LIFESPAN//10+1)], rotation=0)
    plt.yticks([i+0.5 for i in range(NB_DEVICES)], ["Device" + str(i) for i in range(1, NB_DEVICES+1)], rotation=0)
    plt.plot([0, SIM_LIFESPAN], [0, 0], color = "white", linewidth=0.5)
    plt.plot([0, SIM_LIFESPAN], [NB_DEVICES, NB_DEVICES], color = "white", linewidth=0.5)
    for i in range(1, NB_DEVICES):
        plt.plot([0, SIM_LIFESPAN], [i, i], color = "grey", linewidth=0.35)
    plt.title("Simulation for " + str(NB_DEVICES) + " devices with lifespan " + str(SIM_LIFESPAN))
    plt.xlabel("Time (in epochs)")
    plt.axis([0, SIM_LIFESPAN, 0, NB_DEVICES])
    plt.pause(0.1)
    camera.snap()


#--------------------------SIMULATION OF THE NETWORK--------------------------------#

def run():
    #INITIALIZING Simulation, Devices and Monitor
    devicesList = [Device(i+1, w_e = 1, theta_e = NB_DEVICES, lambda_e = 1, p_e = 0.5) for i in range(NB_DEVICES)]

    mainMonitor = Monitor()



    #--------------------------ALGORITHM ALOHA--------------------------------#

    aloha = Aloha(devicesList)

    aloha.run_algorithm(ITERATIONS_ALOHA, eta = 0.5)
    print("result for p_e's : ", aloha.display_pe())
    print("result for lambda_e's : ", aloha.display_lambda())

    #aloha.plot_lambda(ITERATIONS_ALOHA)


    #-------------------------------------------------------------------------#



    #INITIALIZING PLOTTING AND VISUAL REPRESENTATION
    # create figure object
    #fig = plt.figure(figsize=(15, 4), dpi=200)
    # load axis box
    #ax = plt.axes()
    #set x and y axis vals
    x = np.arange(0, SIM_LIFESPAN + 1, 1)
    y = np.arange(0, NB_DEVICES + 1, 1)
    #plt.xticks(x)
    #plt.yticks(y)
    x_vals = []
    y_vals = []
    listOfPatches = []
    #setup snpashot cam
    #snap = Camera(fig)
    
    sim = Simulation(devicesList, SIM_LIFESPAN, SIM_TF)
    sim.start()

    sim.predictDevices(SIM_WAITING_TIME)
    #Main Simulation Loop
    while(sim.isRunning):
        
        sim.activateDevices(mainMonitor, SIM_WAITING_TIME)
        #print(sim.activatedDevicesList)


        #display(sim.activatedDevicesList, snap)
        print(sim.status())
        
        sim.epochs += 1
        
        if(sim.isEnd()):
            sim.end()
    results = Results(devicesList, SIM_LIFESPAN)
    results.modifyCommsHistories()
    #results.printResultsAoI()
    #results.plotAoIGraphs(2) # Be careful with high values of NB_DEVICES !!!
    return results.returnMoyAoIGlobal()
    
listAverageAoI = []
for i in range(NB_SIMULATIONS):
    moyAoIi = run()
    listAverageAoI.append(moyAoIi)

#-----------------------------------------------------------------------------------#

#--------------------------RESULTS OF THE SIMULATION--------------------------------#
print(sum(listAverageAoI)/len(listAverageAoI))
#results = Results(devicesList, SIM_LIFESPAN)
#results.modifyCommsHistories()
#results.plotAoIGraphs(2) # Be careful with high values of NB_DEVICES !!!
#results.printResultsAoI()


#print(mainMonitor.db)
#animation = snap.animate()
#animation.save('animation.gif', writer='PillowWriter', fps=2)
#-----------------------------------------------------------------------------------#
