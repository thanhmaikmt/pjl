from simulation import *
import pygame 
from fontmanager import  *

#     get the gravity pod to hover at y=yHover
#

yHover   =  300
dydtMin  = -100
dydtMax  =  10
XREF = 350
YREF = 400
X_circ=350
Y_circ=400
RAD_circ=200

class Painter:
    
    def __init__(self):
        self.postDraw=None       # define this function to draw on top!
        
    def preDraw(self,screen):    # called before simulation draws to screen
       #  print "predraw"
        fontMgr = cFontManager(((None, 20), (None, 48), ('helvetica', 24)))
        pygame.draw.circle(screen,(255,255,255),(X_circ,Y_circ),RAD_circ,2)
        fontMgr.Draw(screen, None, 20,"x",(XREF,YREF), (255,255,255) )       
class HoverControl:
    def toString(err_x,err_ang,state,control):
        ret= str("Input ")+str(state.dxdt)+","+ str(err_x)+ ","+ str(state.dydt) + "," + str(state.ang)+ ","+ str(state.dangdt)+ ","+ str(err_ang)+ ","
    
        ret=ret + str("Control ") + str(control.up)+"," +str(control.down)+","+ str(control.left)+ ","+ str(control.right) +" \n"
        
        return ret
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
        
        
        err_y = state.y-YREF
            
        control.up= (err_y/(abs(state.dydt+0.01))) *0.05
        if state.y > YREF:
            if state.dydt>0:
                control.up= (state.dydt)*err_y
        
        err_x = state.x-XREF
    
       
  
        err_x = state.x-XREF
        if err_x > 10:
            control.left=(0.01/300)*err_x
            if abs(state.dxdt)>2:
                control.left=0
        elif -10<err_x<10:
            print "almost there"
        else:
            control.right=(0.01/300)*err_x
            if abs(state.dxdt)>2:
                control.right=0
        err_ang = pi-state.ang
        if err_ang<=0.01:
            control.right=abs(err_ang)
            if abs(state.dangdt)>0.04:
                control.left=abs(err_ang*state.dangdt*5)
                #pod.ang=pi

        else:
            control.left=abs(err_ang)
            if abs(state.dangdt)>0.04:
                control.right=abs(err_ang*state.dangdt*5)
                #pod.ang=pi
                
        if err_x<0:
            control.left=abs(err_x/100000)
        else:
            control.right=err_x/100000
        
        print "angvel:: "+str(state.dangdt)
        print "angerr:: "+str(err_ang)
        print "L: "+ str(control.left)+" R " + str(control.right)
        

        
        if training:
            file.write(toString(err_x,err_ang,state,control))
        
        
        return control

training=False
file = open("traingData","w")

dt          =.1
brain       = HoverControl()
nSensors    = 0
sensorRange = 2000
pod         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
pods        = [pod]
world       = World("rect_world.txt",pods)
sim         = Simulation(world,dt)

painter = Painter()
sim.painter=painter

#uncomment the next line to hide the walls.
#sim.world.blind=True

sim.run()
