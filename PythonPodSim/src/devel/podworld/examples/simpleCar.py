
from simulation import *
from math import  *
from pods import *

from world import *
from gui import  *


# Example of a user controller
# This defines the class
class CursorControl:

    # all controller must implement process
    # this will get called each time step of the simulation
    # it returns a "control" object which is used to control the pod
    
    def process(self,pod,dt):

                
        # what happens here is up to you
        # This example looks at  key press to set the control

        control=Control()
        keyinput = gui.get_pressed()    

        #  ----  Just to demonstrate what information is available to use for input to the control
        if keyinput[pg.K_x]:
            # -------  This code prints out all the available information about the state of the pod
            for attr, value in pod.state.__dict__.iteritems():
                print str(attr)+ " "+ str(value) 
        

        if keyinput[pg.K_z]:
            # print the sensor information
            for  sensor in pod.sensors:
                    print sensor
    
        # --- use keypresses to determine control
        if keyinput[pg.K_LEFT]:
            control.left=.4

        if keyinput[pg.K_RIGHT]:
            control.right=.4

        if keyinput[pg.K_UP]:
            control.up=1

        if keyinput[pg.K_DOWN]:
            control.down=1

        return control


# Creates an "instance" of a CursorControl
control=CursorControl()


# create a CarPod with 
# --- no snesors (empty list)  
# --- it will use control
# --- (255,0,0)   is the colour r,g,b

sensors=[]       #   no sensors
pod=CarPod((255,0,0))
pod.addSensors(sensors)
pod.setController(control)

# pod=CarPod([],control,(255,255,0))
# we need to pass a list of pods to the world when we create it

pods=[pod]     #  list with just one element  

    
# world definition file
#worldFile="carCircuit.world"
worldFile="../worlds/carCircuit.world"
# Time step
dt=0.1   

# create  the world
myWorld=World(worldFile,dt,pods)

sim=Simulation(myWorld,"My Title")
sim.run()