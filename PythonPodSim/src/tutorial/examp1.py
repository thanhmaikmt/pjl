
from simulation import *
from math import  *
import gui

class MyWorld:
    
    def __init__(self,name,dt):
        self.name=name
        self.dt=dt
        self.time=0
        
        
    def dimensions(self):
        return 200,200
    
    def start(self):
        print self.name+" START"
        
    def step(self):
        self.time+=self.dt
        self.y=50*cos(self.time)
        self.x=50*sin(self.time)
        
        
    def draw(self,screen):
        x1=100
        y1=100
        x2=x1+self.x
        y2=y1+self.y
        col=(255,0,0)
        thick=1
        gui.draw_line(screen,x1,y1,x2,y2,col,thick)
        col=(0,255,0)
        gui.draw_string(screen,"time="+str(self.time),(20,20),col,16)
        
        
        


dt=0.1    # time step in secs
title="PaulsWorld"
myWorld=MyWorld(title,dt)

sim=Simulation(myWorld,"My Title",dt)
sim.run()