import random
from device import Device
from monitor import Monitor
from simulation import Simulation

#CSTES
DEVICES_NUMBER = 10
SIM_LIFESPAN = 20
SIM_TF = 3

#initialization for Simulation, Monitor, Devices
devicesList = [Device(random.randrange(0,DEVICES_NUMBER)) for i in range(DEVICES_NUMBER)]
mainMonitor = Monitor()
sim = Simulation(devicesList, SIM_LIFESPAN, SIM_TF)
sim.start()


while(sim.isRunning):
    sim.epochs += 1
    sim.tfValue += 1

    if(sim.isTF()):
        print('TF achieved')

    if(sim.isEnd()):
        sim.end()
    