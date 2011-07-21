'''
Created on 4 Dec 2010

@author: pjl
'''

from simulation import *
import pygame 

#
#    Manual drive a car around a track
#


class CursorControl:

    def process(self,sensor,state,dt):
        control=Control()
        keyinput = pygame.key.get_pressed()

        if keyinput[pg.K_LEFT]:
            control.left=1

        if keyinput[pg.K_RIGHT]:
            control.right=1

        if keyinput[pg.K_UP]:
            control.up=1

        if keyinput[pg.K_DOWN]:
            control.down=1
        if state.ang == 180 and state.x == 60:
            control.up=1
        elif state.y == 600 and 60 < state.x < 240:
               control.left =1
               
        return control



dt          =.1
brain       = CursorControl()
nSensors    = 4
sensorRange = 2000
pod         = CarPod(nSensors,sensorRange,brain,(255,0,0))
#pod         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
pods        = [pod]
world       = World("../rect_world.txt",pods)
sim         = Simulation(world,dt)

#uncomment the next line to hide the walls.


#sim.world.blind=True
#sim.frameskipfactor=10


sim.run()
