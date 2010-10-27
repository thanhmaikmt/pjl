from simulation import *
import pygame 

#
#    Manual drive a car around a track
#

def toString(sensors,state,control):
    ret=str(state.dxdt)+" "+ str(state.dydt) + " " + str(state.ang)+ " "
    for s in sensors:
        ret = ret + str(s.val) + " "
        
    ret=ret + str(control.up)+" "+ str(control.left)+ " "+ str(control.right) +"\n"
        
    return ret

class CursorControl:

    def process(self,sensor,state,dt):
        control=Control()
        keyinput = pygame.key.get_pressed()

        global training

        if keyinput[pg.K_t]:
            training = not training
           
            if not training:
                print "closing file "
                file.close()
            else:
                print "training "
                 
        if keyinput[pg.K_LEFT]:
            control.left=.4

        if keyinput[pg.K_RIGHT]:
            control.right=.4

        if keyinput[pg.K_UP]:
            control.up=1

        if keyinput[pg.K_DOWN]:
            control.down=1
    
        if training:
            file.write(toString(sensor,state,control))

        return control




training=False
file = open("traingData","w")

dt          =.1
brain       = CursorControl()
nSensors    = 4
sensorRange = 2000
pod         = CarPod(nSensors,sensorRange,brain,(255,0,0))
# pod.slip_speed_max=1     # testing ice
#pod         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
pods        = [pod]
world       = World("world.txt",pods)
sim         = Simulation(world,dt)

#uncomment the next line to hide the walls.


#sim.world.blind=True
#sim.frameskipfactor=10


sim.run()
