'''
Created on 21 Dec 2010

@author: pjl
'''




    
# Define some classes
import time
import gui



class Painter:   # use me to display stuff
    
    def __init__(self,sim,run_name):
        self.preDraw=None       # define this function to draw on top!      
        self.last_time=time.time()
        self.last_ticks = 0
        self.sim=sim
        self.run_name=run_name
        
    def postDraw(self,screen):
        Y=20
        X=20
        sim=self.sim
        
        
        tot_ticks=sim.ticks
        ticks=tot_ticks-self.last_ticks
        
        tot_time=time.time()
        
        delta=tot_time-self.last_time
        ticks_per_sec=ticks/delta
        
        self.last_time=tot_time
        self.last_ticks=tot_ticks
                
        FMT=sim.world.reaperPlug.FIT_FMT
        pool=sim.world.pool
        tickRateStr="%8.1f" % ticks_per_sec
           
        if pool != None:
        #    avFitStr=FMT % pool.average_fitness()
         
            bestStr=pool.displayString()
        
        #flukeStr=topToString(pool.fluke_list)
        
        #provenStr=topToString(pool.proven_list)
        
        
            str1=self.run_name+' pool size :'+ str(len(sim.world.agents))+\
                           '   ticks :'+ str(sim.ticks) +\
                           '   best :'+ bestStr +\
                           '   ticks/sec :'+tickRateStr+"    "
        else:
            str1=self.run_name+ '   ticks/sec :'+tickRateStr+"    "

       # print str1
        gui.draw_string(screen, str1,(X,Y), (0,255,0),20 )
        sim.world.reaperPlug.postDraw(screen,gui.fontMgr)
        