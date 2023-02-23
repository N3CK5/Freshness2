import random
import time
from device import Device
from monitor import Monitor
from simulation import Simulation

#CSTES
DEVICES_NUMBER = 4
SIM_LIFESPAN = 10
SIM_TF = 2

#initialization for Simulation, Monitor, Devices
devicesList = [Device(random.randrange(0,DEVICES_NUMBER)) for i in range(DEVICES_NUMBER)]
mainMonitor = Monitor()
sim = Simulation(devicesList, SIM_LIFESPAN, SIM_TF)
sim.start()

while(sim.isRunning):
    time.sleep(1)
    sim.epochs += 1
    sim.tfValue += 1

    sim.predictDevices()


    if(sim.isTF()):
        print('TF achieved')
        sim.activateDevices(mainMonitor)


    if(sim.isEnd()):
        sim.end()
    
    print("EPOCH DONE")

print(mainMonitor.db)
    