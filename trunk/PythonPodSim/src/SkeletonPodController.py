from simulation import *
from backpropbrain import  *


#  
#
# WARNING UNTESTED CODE   .   . .  .  . . .
#
#    Brain to drive a car around a track
#

fileName="carTraining.txt"

class BrainControl:

    def __init__(self):
        # load the trained net       
        file=open("greystuff","r")
        self.net=loadBrain(file)
        
    def process(self,sensor,state,dt):
        control=Control()
            
    
        # create the input for the net 
        input=[state.dxdt,state.dydt,state.ang]
        
        for s in sensor:
            input.append(s.val)
            
        # activate the net to get output    
        output=self.net.ffwd(input)
       
        # assign values to the controllers
        control.up=output[0]
        control.down=output[1]
     #   control.left=output[2]
     #   control.right=output[3]
        
        return control



dt          =.1
brain       = BrainControl()
nSensors    = 6
sensorRange = 2000
pod         = CarPod(nSensors,sensorRange,brain,(255,0,0))

pod.ang=pi/2

# pod.slip_speed_max=1     # testing ice
#pod         = GravityPod(nSensors,sensorRange,net,(255,0,0))

pods        = [pod]
world       = World("car_world.txt",pods)
sim         = Simulation(world,dt)

#uncomment the next line to hide the walls.
#sim.world.blind=True
#sim.frameskipfactor=10


sim.run()
