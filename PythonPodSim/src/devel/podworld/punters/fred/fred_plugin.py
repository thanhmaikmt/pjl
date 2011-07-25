import sys
import gui
import world
from pods import *
import simulation
import fred_util


class Controller:

    # called by simulation to control the pod
    def process(self,pod,dt):
        
        
        control=Control()
        
        keyp = gui.get_pressed()
                
        if keyp[gui.keys.K_a]:
            control.left=1

        if keyp[gui.keys.K_d]:
            control.right=1

        if keyp[gui.keys.K_w]:
            control.up=1

        if keyp[gui.keys.K_x]:
            control.down=1
        #print control.left,control.right,control.up,control.down
        
        return control


def equip_car(car):
    
    
    fin=open("text.txt","r")
    text=fin.read()
    print text
    fred_util.my_util()
    controller=Controller()
    car.setController(controller)
    car.setColour((0,255,0))
    
    
    
if __name__ =="__main__":
    pods=[]
    pod   = CarPod()
   
    # call the pluginto equip the car 
    equip_car(pod)
    pods.append(pod)
    

    
###  START OF PROGRAM

    dt    = .1
    world = world.World("../../rectWorld.world",dt,pods)
    sim   = simulation.Simulation(world,"Example")
    sim.run()