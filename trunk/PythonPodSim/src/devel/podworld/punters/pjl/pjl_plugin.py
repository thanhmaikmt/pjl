import gui
from pods import *

import pjl_util


class Controller:

    # called by simulation to control the pod
    def process(self,pod,dt):
        
        control=Control()
        
        keyp = gui.get_pressed()
                
        if keyp[gui.keys.K_LEFT]:
            control.left=1

        if keyp[gui.keys.K_RIGHT]:
            control.right=1

        if keyp[gui.keys.K_UP]:
            control.up=1

        if keyp[gui.keys.K_DOWN]:
            control.down=1
        #print control.left,control.right,control.up,control.down
        
        return control


def equip_car(car):
    
    
    fin=open("text.txt","r")
    text=fin.read()
    print text
    pjl_util.my_util()
    controller=Controller()
    car.setController(controller)
    car.setColour((255,0,0))
    