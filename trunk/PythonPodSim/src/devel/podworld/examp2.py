
from simulation import *
from math import  *
from pods import *

from world import *
from gui import  *

        
# Time step
dt=0.1    

# world definition file
worldFile="carCircuit.world"


# Example of a user controller
# This defines the class
class CursorControl:

    # all controller must implement process
    def process(self,pod,dt):
        
        # what happens here is up to you
        # I just use the user key presses to set the outputs.
        control=Control()
        keyinput = gui.get_pressed()    
    
        if keyinput[pg.K_LEFT]:
            control.left=.4

        if keyinput[pg.K_RIGHT]:
            control.right=.4

        if keyinput[pg.K_UP]:
            control.up=1

        if keyinput[pg.K_DOWN]:
            control.down=1

        return control

# this creates an "instance" of the class
control=CursorControl()


# create a CarPod with 
# --- no snesors (empty list)  
# --- it will use control
# --- (255,0,0)   is the colour r,g,b
pod=CarPod([],control,(255,0,0))

# we need to pass a list of pods to the world when we create it
pods=[pod]     # 

# create  the world
myWorld=World(worldFile,dt,pods)

sim=Simulation(myWorld,"My Title")
sim.run()