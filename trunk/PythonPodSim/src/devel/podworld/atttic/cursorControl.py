from simulation import *

from pods import *
from world import  *
from agent import *

import gui

class CursorControl:

    def process(self,pod,dt):
        
        control=Control()
        #print "1"
        
        keyp = gui.get_pressed()
        
        #print "2"
        
        # gui.get_pressed()
        
        #print pg
       
       
                
        if keyp[gui.keys.K_LEFT]:
            control.left=1

        if keyp[gui.keys.K_RIGHT]:
            control.right=1

        if keyp[gui.keys.K_UP]:
            control.up=1

        if keyp[gui.keys.K_DOWN]:
            control.down=1

        #print control.left,control.right,control.up,control.down
        
        return control


dt          =.05
plug       = CursorControl()
nSensors    = 6
sensorRange = 2000
pod         = CarPod([],None,plug,(255,0,0))

pod.ang=pi/2

# pod.slip_speed_max=1     # testing ice
#pod         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
agents=[]
agents.append(Agent(pod))
 

world       = World("carCircuit.world",dt)
sim         = Simulation(world,agents,None,None,None,"CursorControl")

#uncomment the next line to hide the walls.
#sim.world.blind=True
#sim.frameskipfactor=10


sim.run()