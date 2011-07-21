import pygame
from simulation import *

#
#  Cursor control UP/DOWN with some collision protection using snsors
#



class AutoControl:

    def __init__(self):
        self.targetState = None
        self.vel=100
        self.velHyst=2
        self.dd=100

    def process(self,sensor,state,dt):

        control=Control()
        
        keyinput = pygame.key.get_pressed()
        
        if keyinput[pg.K_LEFT]:
            pass

        if keyinput[pg.K_RIGHT]:
            pass

        if state.dydt > self.velHyst and sensor[len(sensor)/2].val < self.dd:
            control.up=1
            return control
     

        if keyinput[pg.K_UP] and  state.dydt > -self.vel:
            if state.dydt < -self.velHyst and sensor[0].val < self.dd:
                print "UP collide :",sensor[0].val
                return control
            control.up=1

        elif keyinput[pg.K_DOWN]:
            if state.dydt < self.vel:
                control.up=0
            else:
                control.up=1

        else:
            if state.dydt > self.velHyst:
                control.up=1

    #    print state.dydt, control.up
        
        return control



dt          =.1
brain       = AutoControl()
nSensors    = 40
sensorRange = 2000
pod         = GravityPod(nSensors,sensorRange,brain,(0,255,255))
pods        = [pod]
world       = World("rect_world.txt",pods)
sim         = Simulation(world,dt)

#uncomment the next line to hide the walls.
#sim.world.blind=True

sim.run()
