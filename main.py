from device import Device
from monitor import Monitor
from simulation import Simulation
from Aloha import Aloha
import numpy as np
import math

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from celluloid import Camera

#CONSTANTS
NB_DEVICES = 5
SIM_LIFESPAN = 100
SIM_TF = 3
ITERATIONS_ALOHA = 60


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
fig = plt.figure(figsize=(15, 4), dpi=200)
# load axis box
ax = plt.axes()
#set x and y axis vals
x = np.arange(0, SIM_LIFESPAN + 1, 1)
y = np.arange(0, NB_DEVICES + 1, 1)
plt.xticks(x)
plt.yticks(y)
x_vals = []
y_vals = []
listOfPatches = []
#setup snpashot cam
#snap = Camera(fig)

#Display function for processing data and displaying it with matplotlib
def display(activatedDevicesList, camera):
    
    for device in activatedDevicesList:
        rectangle = Rectangle((sim.epochs, device['id'] - 1), 1, 1, edgecolor = 'green', facecolor='none', lw = 1)
        listOfPatches.append([device['id'],rectangle])
    
    for patch in listOfPatches:
        ax.add_patch(patch[1])
        rx, ry = patch[1].get_xy()
        cx = rx + patch[1].get_width()/2.0
        cy = ry + patch[1].get_height()/2.0
        #ax.annotate('device  {}'.format(patch[0]), (cx, cy), color='green', weight='bold', fontsize=6, ha='center', va='center')
        
    plt.pause(0.1)    
    camera.snap()


#--------------------------SIMULATION OF THE NETWORK--------------------------------#

sim = Simulation(devicesList, SIM_LIFESPAN, SIM_TF)
sim.start()

#Main Simulation Loop
while(sim.isRunning):

    sim.predictDevices()
    
    #wait for a number of epoch
    sim.activateDevices(mainMonitor)
    #print(sim.activatedDevicesList)


    #display(sim.activatedDevicesList, snap)
    print(sim.status())
    
    sim.epochs += 1
    
    if(sim.isEnd()):
        sim.end()
    
for i in range(len(devicesList)):
    print(devicesList[i].p_e)
    devicesList[i].comms_history = [element[0] for element in devicesList[i].comms_history if len(element) > 1]
    

for i in range(NB_DEVICES):
    for j in range(NB_DEVICES):
        if i > j:
            ensI = set(devicesList[i].comms_history)
            ensJ = set(devicesList[j].comms_history)
            ensI1 = ensI - ensJ
            ensJ1 = ensJ - ensI
            lI = list(ensI1)
            lJ = list(ensJ1)
            lI.sort()
            lJ.sort()
            devicesList[i].comms_history = lI
            devicesList[j].comms_history = lJ


fig, axs = plt.subplots(NB_DEVICES, sharex=True, sharey=True)
fig.suptitle("Age of Information for each device")


X = [[] for k in range(NB_DEVICES)]
Y = [[] for k in range(NB_DEVICES)]
colorGraphs = {0: 'g-', 1:'b-', 2:'r-',3:'c-', 4:'k-', 5:'m-'}

for k in range(NB_DEVICES):
    X[k].append(0)
    Y[k].append(0)
    if len(devicesList[k].comms_history) == 0:
        X[k].append(SIM_LIFESPAN)
        Y[k].append(SIM_LIFESPAN)
        axs[k].plot(X[k], Y[k], colorGraphs[k%len(colorGraphs)])
        continue
    X[k].append(devicesList[k].comms_history[0])
    Y[k].append(devicesList[k].comms_history[0])
    i = -1
    for i in range(len(devicesList[k].comms_history) - 1):
        X[k].append(devicesList[k].comms_history[i])
        Y[k].append(0)
        X[k].append(devicesList[k].comms_history[i+1])
        Y[k].append(devicesList[k].comms_history[i+1] - devicesList[k].comms_history[i])
        X[k].append(devicesList[k].comms_history[i+1])
        Y[k].append(0)
    if devicesList[k].comms_history[i+1] < SIM_LIFESPAN - SIM_TF:
        X[k].append(devicesList[k].comms_history[i+1])
        Y[k].append(0)
        X[k].append(SIM_LIFESPAN)
        Y[k].append(SIM_LIFESPAN - devicesList[k].comms_history[i+1])
    axs[k].plot(X[k], Y[k], colorGraphs[k%len(colorGraphs)])

plt.setp(axs[-1], xlabel='Time (in epochs)')
for i in range(NB_DEVICES):
    plt.setp(axs[i], ylabel='AoI (in epochs)')

plt.savefig("AOI_graph.jpg")


#print(mainMonitor.db)
#animation = snap.animate()
#animation.save('animation.gif', writer='PillowWriter', fps=2)

