#%% 

import random
import time
from device import Device
from monitor import Monitor
from simulation import Simulation
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from celluloid import Camera

#plt.style.use('fivethirtyeight')

NB_DEVICES = 4
SIM_LIFESPAN = 10
SIM_TF = 2


#initialization for Simulation, Monitor, Devices
devicesList = [Device(i+1) for i in range(NB_DEVICES)]
mainMonitor = Monitor()
sim = Simulation(devicesList, SIM_LIFESPAN, SIM_TF)
sim.start()


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

#setup snpashot cam
snap = Camera(fig)

def display(activatedDevicesList, camera):
    print("sortie fonction display : ", activatedDevicesList)
    for device in activatedDevicesList:
        rectangle = Rectangle( (sim.epochs, device['id'] - 1), 1, 1, edgecolor = 'green', facecolor='none', lw = 1)
        ax.add_patch(rectangle)
        rx, ry = rectangle.get_xy()
        cx = rx + rectangle.get_width()/2.0
        cy = ry + rectangle.get_height()/2.0
        ax.annotate('device  {}'.format(device['id']), (cx, cy), color='green', weight='bold', fontsize=6, ha='center', va='center')
    
    plt.pause(0.1)    
    camera.snap()
    
while(sim.isRunning):

    sim.predictDevices()
    sim.activateDevices(mainMonitor)
    
    print(sim.activatedDevicesList)


    display(sim.activatedDevicesList, snap)
    print(sim.status())
    
    sim.epochs += 1
    sim.tfValue += 1
    
    if(sim.isEnd()):
        sim.end()
        

#print(mainMonitor.db)
animation = snap.animate()
animation.save('animation.gif', writer='PillowWriter', fps=2)

