
from simulation import *
from math import  *
from world import *
import gui

        
        


dt=0.1    # time step in secs
title="PaulsWorld"
myWorld=World(title,dt)

sim=Simulation(myWorld,"My Title",dt)
sim.run()