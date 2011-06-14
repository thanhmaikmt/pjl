from math import *
import gui


class Simulation:
    """ The simulation class is responsible for running the Pod World.
     """

    def __init__(self,world,run_name):
        
        #: world     a World
        #: agents    list of agents
        
   
        self.admin=None
        self.ticks=0
        self.slowMotionFactor=1.0
        self.world = world
        w,h=(self.world.dimensions())
        dim_world = (w+20,h+20)
        self.frameskipfactor=1
        self.frameskipcount=1
        self.painter=None
        
        self.screen = gui.init_surface(dim_world,run_name)
        
        
        self.log_file=open(run_name+".log","w")
        self.run_name=run_name
    
        
   
    def setAdmin(self,admin):
        self.admin=admin
   
            
    def run(self):
        """ start the simulation  
        """
        dt=self.dt
        clock = gui.clock()
        frameRate=1.0/dt/self.slowMotionFactor
        self.tick_count=0
        
        self.world.start()
         
            
        
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
            
            
            self.ticks += 1
            self.world.step()
            
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
                
                
