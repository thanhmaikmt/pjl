# To change this template, choose Tools | Templates
# and open the template in the editor.


import pygame
from simulation import *
import copy

yHover   =  300
dydtMin  = -100
dydtMax  =  10

class AutoControl:


    def __init__(self):
        self.targetState = None
        self.vel=100
        self.velHyst=2

    def process(self,sensor,state,dt):

       

        control=Control()
        
        keyinput = pygame.key.get_pressed()
        
        if keyinput[pg.K_LEFT]:
            pass

        if keyinput[pg.K_RIGHT]:
            pass


        if keyinput[pg.K_UP] and  state.dydt > -self.vel:
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
pod         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
pods        = [pod]
world       = World("rect_world.txt",pods)
sim         = Simulation(world,dt)

#uncomment the next line to hide the walls.
#sim.world.blind=True

sim.run()
