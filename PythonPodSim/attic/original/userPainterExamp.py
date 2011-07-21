from simulation import *
from fontmanager import *
#
#     get the gravity pod to hover at y=yHover
#

yHover   =  300
dydtMin  = -100
dydtMax  =  10
yError   =  0 

class Painter:
    
    def __init__(self):
        #self.postDraw=None       # define this function to draw on top!
           # a font of None means to use the default font
         
        self.fontMgr = cFontManager(((None, 24), (None, 48), ('arial', 24)))
    
    def preDraw(self,screen):    # called before simulation draws to screen
       #  print "predraw"
        col=(255,255,255)
        pg.draw.line(screen,col,(0,yHover),(world.rect.width,yHover),2)
        
    def postDraw(selfself,screen):
        self.fontMgr.Draw(screen, None, 24, ' Error is '+str(yError), (20, 20), col)
 
     
class HoverControl:

    def process(self,sensor,state,dt):

        control=Control()

        global yError
        
        yError=state.y-yHover
        
        if state.y > yHover:
           if state.dydt > dydtMin:
              control.up=1

        if state.dydt > dydtMax:
            control.up=1

        return control



dt          =.1
brain       = HoverControl()
nSensors    = 40
sensorRange = 2000
pod         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
pods        = [pod]
world       = World("small_rect_world.txt",pods)
sim         = Simulation(world,dt)

painter = Painter()
sim.painter=painter

#uncomment the next line to hide the walls.
#sim.world.blind=True

sim.run()
