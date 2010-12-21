'''
Created on 21 Dec 2010

@author: pjl
'''


from agent import *
from simulationMP import *
from world import  *
from painter import *
from pool import  *
import gravityplug
from admin import  *

# 
plug=gravityplug.GravityPlug()

dt=.1

###  START OF PROGRAM

world       = World(plug.WORLD_FILE,dt)

pool=Pool(world,plug)    #  create a pool for fittest networks

agents=[]        #  pods on the circuits

POP_SIZE=10
for i in range(POP_SIZE):     # create initial population on the circuit
    agents.append(Agent(plug,i))
  
admin       = Admin()
sim         = Simulation(world,agents,plug,pool,admin,plug.RUN_NAME)

# register the painter to display stuff
sim.painter = Painter(sim,plug.RUN_NAME)

# go go go  ..........
sim.run()
