from math import *
import multiprocessing as mp
from copy import *
import gui


class Simulation:
    """ The simulation class is responsible for running the Pod World.
     
    :param world:    World.
    :param agents:   list of Agents.
    :param plug:     plugin class.
    :param pool:     Pool.
    :param admin:    Admin.
    :param run_name:  string used for log files etc 
    """

    def __init__(self,world,agents,plug,pool,admin,run_name):
        
        #: world     a World
        #: agents    list of agents
        
   
        self.admin=admin
        self.ticks=0
        self.slowMotionFactor=1.0
        self.world = world
        self.agents=agents
        dim_world = (self.world.rect.width+20, self.world.rect.height+20)
        self.frameskipfactor=1
        self.frameskipcount=1
        self.painter=None
        
        self.screen = gui.init_surface(dim_world)
        
        
        self.plug=plug
        self.pool=pool
        self.log_file=open(run_name+".log","w")
        self.run_name=run_name
    
        
    def reaper(self,pod):
        if self.plug == None:
            return False 
        return self.plug.reaper(pod,self)        
       
        
    def step(self):
        self.ticks += 1
                         
      
      
        # send "step" message to all agents
        # this can be multithreaded  
        for agent in self.agents:
           agent.stepInit()
        
    
        # wait for all agents to report back         
        for agent in self.agents:
            agent.waitForDone()
            #print " state is: ", state     
        
        # back to a single thread now
        for agent in self.agents:
            agent.admin(self)
            
            
    def run(self):
        """ start the simulation  
        """
        dt=self.world.dt
        clock = gui.clock()
        frameRate=1.0/dt/self.slowMotionFactor
        self.tick_count=0
        
        for agent in self.agents:
            self.world.insertPod(agent.pod)
            agent.start()
            
         
            
        
       # the event loop also loops the animation code
        while True:
            
            self.frameskipcount -= 1
            self.tick_count += 1
            display= self.frameskipcount == 0 and self.frameskipfactor != 0

            if display:
                clock.tick(frameRate)
                self.frameskipcount=self.frameskipfactor

            if display or (self.tick_count%100)==0:
                gui.grab_events()
                if self.admin != None:
                    self.admin.process(self)
                  
            if gui.check_for_quit():
                break
              
            self.step()
            
            if display:
                self.screen.fill((0,0,0))
                
                if self.painter != None:
                    if self.painter.preDraw != None:
                        self.painter.preDraw(self.screen)
                    
                self.world.draw(self.screen)
                      
                
                if self.painter != None:
                    if self.painter.postDraw != None:
                        self.painter.postDraw(self.screen)
                gui.blit(self.screen)
                
                
