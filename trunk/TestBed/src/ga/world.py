'''
Created on 28 Jun 2011

@author: pjl
'''


from math import *
import random
import gui

thresh=10 
nGenerator=10
nConsumer=30
big=1e7

maxDemmand=100
maxGen=1000
maxLineCap=10000
              # min token value required to build line
tokMax=128
overhead=1000
costPerCapacity=100


class World:
    
    def __init__(self):
        self.consumers=[]
        self.generators=[]
        self.lines=[]
       
        for i in range(nConsumer):
            demmand=random.random()*maxDemmand
            x,y=gui.random_point();   
            self.consumers.append(Consumer(demmand,x,y))
            
            
        for i in range(nGenerator):
            gen=random.random()*maxGen
            x,y=gui.random_point();
            self.generators.append(Generator(gen,x,y))
         
        for c in self.consumers:
            for g in self.generators:
                self.lines.append(Line(c,g))
                
    
    def evaluate(self,gene):   # number correct
        c_shortfall=0.0
        c_surplus=0.0
        l_cost=0.0
        g_cost=0.0
        
        cnt=0
        for c in self.consumers:
            for l in c.lines: 
                tok=gene[cnt]
                l.setToken(tok)
                cnt += 1

        for c in self.consumers:
            sup=c.supply()-c.demand
            if (sup > 0):
                c_surplus += sup
            else:
                c_shortfall -= sup
            
            l_cost += c.line_cost()
        
        g_shortfall=0.0
        g_sup=0
        
        for g in self.generators:
            demmand = g.demmand()
            if demmand != 0:
                g_cost += g.cost
                sup=g.capacity-demmand
                if sup > 0:
                    g_sup += sup
                else:
                    g_shortfall -= sup
            
        fit=0.0
        if c_shortfall > 0:   
            fit -= big+c_shortfall
        
        if g_shortfall > 0:
            fit -= big+g_shortfall
   
        fit -=  (g_cost + l_cost)  
        
        gene.fit=fit
        
class Node:

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.lines=[]

        
class Generator(Node):
    def __init__(self,cost,x,y):
        Node.__init__(self, x, y)
        self.cost=cost


class Consumer(Node):
    def __init__(self,demmand,x,y):
        Node.__init__(self, x, y)
        self.demmand=demmand

    def supply(self):
        sup=0
        for l in self.lines:
            sup+=l.capacity
        
class Line:
    
    def __init__(self,a,b):
        self.a=a;
        self.b=b;
        a.lines.append(self)
        b.lines.append(self)
        self.dist=sqrt((a.x-b.x)**2 +(a.y-b.y)**2)
        
    def setToken(self,tok):
        if tok < thresh:
            self.capacity=0
            self.cost=0
        else:
            self.capacity=tok*maxLineCap/tokMax
            self.cost=(overhead+tok*costPerCapacity)*self.dist

