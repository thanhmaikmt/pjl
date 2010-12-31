import pygame as pg
from math import *
import multiprocessing as mp
from copy import *



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
        
        pg.init()
        self.admin=admin
        self.ticks=0
        self.slowMotionFactor=1.0
        self.world = world
        self.agents=agents
        dim_world = (self.world.rect.width+20, self.world.rect.height+20)
        self.frameskipfactor=1
        self.frameskipcount=1
        self.painter=None
        self.screen = pg.Surface(dim_world) #
        self.plug=plug
        self.pool=pool
        self.log_file=open(run_name+".log","w")
        self.run_name=run_name
    
        
        modes=pg.display.list_modes()
        dim_display=modes[0]

        sx=dim_display[1]/float(dim_world[1])
        sy=dim_display[0]/float(dim_world[0])
        
        if sx < 1 or sy < 1:
            s=min(sx,sy)/1.2
            self.dim_window=(dim_world[0]*s,dim_world[1]*s)
            print "Small screen: scaling world by ",s

        else:
            self.dim_window=dim_world

        self.display = pg.display.set_mode(self.dim_window)
        pg.display.set_caption('PodSim (press escape to exit)')
        
       
        
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
        clock = pg.time.Clock()
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
                pg.event.pump()
                if self.admin != None:
                    self.admin.process(self)
                
                
            keyinput = pg.key.get_pressed()

            if keyinput[pg.K_ESCAPE] or pg.event.peek(pg.QUIT):
                pg.display.quit()
                break
                # raise SystemExit

                
                
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
                
                zz=pg.transform.scale(self.screen,self.dim_window)
                self.display.blit(zz,(0,0))
                pg.display.flip()
            
