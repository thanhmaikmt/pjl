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
            control.left=.4

        if keyinput[pg.K_RIGHT]:
            control.right=.4

        if keyinput[pg.K_UP]:
            control.up=1

        if keyinput[pg.K_DOWN]:
            control.down=1

        return control



dt          =.1
brain       = CursorControl()
nSensors    = 40
sensorRange = 2000
pod         = CarPod(nSensors,sensorRange,brain,(255,0,0))
pod.slip_speed_max=1     # testing ice
#pod         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
pods        = [pod]
world       = World("rect_world.txt",pods)
sim         = Simulation(world,dt)

#uncomment the next line to hide the walls.


#sim.world.blind=True
#sim.frameskipfactor=10


sim.run()
