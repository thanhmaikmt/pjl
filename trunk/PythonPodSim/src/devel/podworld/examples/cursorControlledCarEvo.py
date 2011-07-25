import gui
from pods import *

class Plugin:


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

    # ???
    def postDraw(self,screen,fontMgr):pass

    # called each step.
    # decide if you pod should be terminated.
    def reaper(self,pod,world):
        if (pod.state.collide_count >0):
             world.init_pod(pod)               # this resets pod to start
             return True
        else:
            return False
    
    def createInitialPods(self):
        
        podlist=[]
        # a controller must implement process(self,pod,dt)
        controller  = self    # this class implements the process function
        sensors     = []      # array of snesors (Empty in this example)
        pod         = CarPod(sensors,controller,(255,0,0))
        podlist.append(pod)
        return podlist
    

def createPlugin():
    return Plugin()