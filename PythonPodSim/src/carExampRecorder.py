from simulation import *
import pygame 
from fontmanager import  *
from math import *

#
#    Manual drive a car around a track
#


recording=False


class Painter:

    def __init__(self):
# a font of None means to use the default font
        self.fontMgr = cFontManager(((None, 24), (None, 48), ('arial', 24)))
    
        self.preDraw=None       # define this function to draw on top!
        
    def postDraw(self,screen):    # called before simulation draws to screen
       #  print "predraw"
        col=(255,255,255)
        if not recording:
            self.fontMgr.Draw(screen, None, 24, ' Hit R to start recording' , (20, 20), col)
        else:     
            self.fontMgr.Draw(screen, None, 24, ' Recording  . . . Hit S to stop recording' , (20, 20), col)
     
def toString(sensors,state,control):
    ret=str(state.dxdt)+" "+ str(state.dydt) + " " + str(state.ang)+ " "
    for s in sensors:
        ret = ret + str(s.val) + " "
        
    ret=ret + str(control.up) + " " + str(control.down)+" "+ str(control.left)+ " "+ str(control.right) +"\n"
        
    return ret

class CursorControl:

    def process(self,sensor,state,dt):
        control=Control()
        keyinput = pygame.key.get_pressed()

        global recording

        if keyinput[pg.K_r]:
            recording = True
            print " recording "
            self.file = open("traingData","wa")
     
        if keyinput[pg.K_s]:
                      
            if recording:
                print "closing file "
                self.file.close()
            recording=False
            
                 
        if keyinput[pg.K_LEFT]:
            control.left=.4

        if keyinput[pg.K_RIGHT]:
            control.right=.4

        if keyinput[pg.K_UP]:
            control.up=1

        if keyinput[pg.K_DOWN]:
            control.down=1
    
        if recording:
            self.file.write(toString(sensor,state,control))

        return control




dt          =.1
brain       = CursorControl()
nSensors    = 4
sensorRange = 2000
pod         = CarPod(nSensors,sensorRange,brain,(255,0,0))
# pod.slip_speed_max=1     # testing ice
#pod         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
pods        = [pod]
world       = World("car_world.txt",pods)
sim         = Simulation(world,dt)


painter = Painter()
sim.painter=painter

#sim.world.blind=True
#sim.frameskipfactor=10

pod.ang = pi/2
sim.run()
