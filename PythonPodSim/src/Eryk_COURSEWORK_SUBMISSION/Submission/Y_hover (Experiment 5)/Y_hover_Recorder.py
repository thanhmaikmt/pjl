from simulation import *
import pygame 

# Use the control alogorithm to collect the data to train the neural net

yHover=300

def toString(sensors,state,control):
    ret= str("Input ") + str(state.dydt)+ " " + str(yHover-state.y)+ " "
    ret= ret
    #for s in sensors:
       # ret = ret + str(s.val) + " "
    
    ret=ret + str("Control ") + str(control.up)+"\n"
        
    return ret

class CursorControl:

    def process(self,sensor,state,dt):
        control=Control()
              
        err = state.y-yHover
            
        control.up= (err/(abs(state.dydt+0.01))) *0.05
        if state.y > yHover:
            
            if state.dydt>0:
                control.up= (state.dydt)*err
            
        if control.up>1:
            control.up=1
        if control.up<0:
            control.up=1
            
        
    
        
        file.write(toString(sensor,state,control))

        return control




file = open("traingData","w")
cont = 0

dt          =.1
brain       = CursorControl()
nSensors    = 2
sensorRange = 2000
#pod         = CarPod(nSensors,sensorRange,brain,(255,0,0))
# pod.slip_speed_max=1     # testing ice
pod         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
pods        = [pod]
world       = World("Y_hover.txt",pods)
sim         = Simulation(world,dt)

#uncomment the next line to hide the walls.


#sim.world.blind=True
#sim.frameskipfactor=10


sim.run()
