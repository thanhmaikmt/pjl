from world import  *
from agent import *
from painter import *
from pool import  *
from admin import  *
from simulation import *
# import cprofile

import cursorControlledCar

plug=cursorControlledCar.createPlugin()
pods=plug.createInitialPods()

###  START OF PROGRAM
dt    = .1
world = World("rect_world.txt",dt,pods,plug)
sim   = Simulation(world,"Example")
sim.run()