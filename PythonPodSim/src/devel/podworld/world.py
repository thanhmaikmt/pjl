'''
Created on 21 Dec 2010

@author: pjl
'''

from config import *
from math import *
from util import *
from agent import *

if NUMPY:
    import numpy

import gui

small=1e-8

class Wall:

    def __init__(self,name):
        self.name=name
        self.segments=[]
        self.maxX=-huge
        self.minX=huge
        self.maxY=-huge
        self.minY=huge

    def read(self,fin):

        points=read_points(fin)

        n=len(points)
        i=0

        while i+3 < n:
            x1=points[i]
            y1=points[i+1]
            x2=points[i+2]
            y2=points[i+3]
            self.segments.append((x1 ,y1, x2, y2))

            if self.maxX < x1:
                self.maxX=x1
            if self.minX>x1:
                self.minX=x1
            if self.maxY < y1:
                self.maxY=y1
            if self.minY>y1:
                self.minY=y1

            i += 2


        self.rect=gui.Rect(self.minX,self.minY,self.maxX-self.minX,self.maxY-self.minY)
       
    
    def len(self):
        return len(self.segments)
    


class World:

    def __init__(self,fileName,dt,pods,reaperPlug=None):

        self.pods=pods
        self.dt=dt
        self.walls=[]
        self.trips=[]
        self.agents=[]
        for pod in pods:
            self.agents.append(Agent(pod))
            
        fin=open(fileName,"r")
        self.rect=gui.Rect(0,0,0,0)
        self.reaperPlug=reaperPlug
        self.blind=False
        self.podang=pi
        
        while True:
            line = fin.readline()
            if len(line)==0:
                break
            if line[0] == '#':
                continue
                
            line.strip()
            tokens=line.split()

            if "wall" in line:
                wall=Wall(tokens[1])
                wall.read(fin)
                self.walls.append(wall)
                self.rect=self.rect.union(wall.rect)

            if  "pod" in line:
                self.read_pod_pos(fin)

        self.build_trip_wires()
        
        p2_x_a=[]
        p2_y_a=[]
        p3_x_a=[]
        p3_y_a=[]
        
        if NUMPY:
            for wall in self.walls:
                for seg in wall.segments:
                    p2_x_a.append(seg[0])
                    p2_y_a.append(seg[1])
                    p3_x_a.append(seg[2])
                    p3_y_a.append(seg[3])
            
            self.p2_x_a=numpy.array(p2_x_a)
            self.p2_y_a=numpy.array(p2_y_a)
            self.p3_x_a=numpy.array(p3_x_a)
            self.p3_y_a=numpy.array(p3_y_a)
         
#        self.walls=N.array(self.walls)
#        self.trips=N.array(self.trips)
        
        
    def reaper(self,pod):
        if self.reaperPlug == None:
            return False 
        return self.reaperPlug.reaper(pod,self)        
    
    def dimensions(self):
        return self.rect.width,self.rect.height
    
    def start(self):
        for agent in self.agents:
            self.insertPod(agent.pod)
            agent.start()
            
        
    def insertPod(self,pod):
        self.pods.append(pod)
        pod.world=self
        self.init_pod(pod)
        
        #
        #
        #pod.start()
        
        
         #   if tryThreading: pod.plant(self,dt)

    def build_trip_wires(self):
        left=None
        right=None
        trips=self.trips
        
        for w in self.walls:
            if "left" in w.name:
                left=w
            if  "right" in w.name:
                right=w
                
        if left != None :
            if len(left.segments) != len(right.segments):
                print " Left and right must have equal number of points"
                
            else:
                for l,r in zip(left.segments,right.segments):
                    trips.append((l[0],l[1],r[0],r[1]))
           
        
        for w in self.walls:
            if "tube" in w.name:
                segs=w.segments
                isegA1=2
                isegB1=len(segs)-2
                cntA=0
                cntB=0
                
                while True:
                    a1=segs[isegA1]
                    b1=segs[isegB1]
                    trips.append((b1[0],b1[1],a1[0],a1[1]))
                    
                    isegA2=isegA1+1
                    isegB2=isegB1-1
                    
                    if isegA2>=isegB2:
                        break
                    
                    a2=segs[isegA2]
                    b2=segs[isegB2]
                    
                    a1b2=dist(a1[0],a1[1],b2[0],b2[1])
                    
                    b1a2=dist(b1[0],b1[1],a2[0],a2[1])
                    
                    a2b2=dist(a2[0],a2[1],b2[0],b2[1])
                    
                    
                    if cntB < 1 and a1b2 < b1a2 and a1b2 < a2b2:
                        isegB1=isegB2
                        cntB += 1
                        cntA  = 0

                    elif cntA < 1 and b1a2 < a1b2 and b1a2 < a2b2:
                        isegA1=isegA2
                        cntA += 1
                        cntB  = 0 
                        
                    else:
                        isegA1=isegA2
                        isegB1=isegB2
                        cntA=0
                        cntB=0
                
                
                # print "POD OK"

    def init_pod(self,pod):
            pod.init()
            state=pod.state
            
            state.x=self.podx
            state.y=self.pody
            state.ang=self.podang
            state.dxt=0
            state.dydt=0
            state.dangdt=0
            state.collide=False
            state.collide_count=0
            state.vel=0.0
            
    def read_pod_pos(self,fin):
        line = fin.readline()
        linelist=line.split(',')

        self.podx = float(linelist[0])
        self.pody = float(linelist[1])
        if len(linelist)>2:
            self.podang=float(linelist[2])*pi/180.0
            
        
        for pod in self.pods:
            self.init_pod(pod)
   
   
    
    def find_closest_intersect(self,p0_x,p0_y,p1_x,p1_y):
     tMin=2
     wallMin=None
     
     if NUMPY:
        
      
        (s,t,dmy)=intersect_numpy(p0_x,p0_y,p1_x,p1_y,self.p2_x_a,self.p2_y_a,self.p3_x_a,self.p3_y_a)
        
        bb = (t >= -small).__iand__(t <= (1+small)).__iand__(s >= -small).__iand__(s <= (1+small))
        
        
        cnt=0;
        for wall in self.walls:
            for seg in wall.segments:    
                if bb[cnt]:
                   if t[cnt] < tMin:
                        tMin=t[cnt]
                        wallMin=wall
                cnt+=1
     else:
        for wall in self.walls:
            for seg in wall.segments:
                p2_x=seg[0]
                p2_y=seg[1]
                p3_x=seg[2]
                p3_y=seg[3]
                (s,t,dmy)=intersect(p0_x,p0_y,p1_x,p1_y,p2_x,p2_y,p3_x,p3_y)
                
                if t >= -small and t <= 1+small and s >= -small and s <= 1+small:
                        if t < tMin:
                            tMin=t
                            wallMin=wall

     return (tMin,wallMin)
     
     
    def step(self):
      
                         
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
            

    def check_collide_with_wall(self,p0_x,p0_y,p1_x,p1_y):
        if p0_x==p1_x and p1_y==p0_y:
            return None,None

        for wall in self.walls:
            for seg in wall.segments:
                p2_x=seg[0]
                p2_y=seg[1]
                p3_x=seg[2]
                p3_y=seg[3]

                (s,t,dmy)=intersect(p0_x,p0_y,p1_x,p1_y,p2_x,p2_y,p3_x,p3_y)
                if s >= 0 and s <= 1 and t >= 0 and t <= 1:
                        #print s,t
                        return wall,s
                
        return None,None

    def count_trips(self,p0_x,p0_y,p1_x,p1_y):
  
  
        # print p0_x,p0_y,p1_x,p1_y
              
        if p0_x==p1_x and p1_y==p0_y:
            return (0,0)


        count_pos = 0
        count_neg = 0
        
        for t in self.trips:
                p2_x=t[0]
                p2_y=t[1]
                p3_x=t[2]
                p3_y=t[3]

                (s,t,fact)=intersect(p0_x,p0_y,p1_x,p1_y,p2_x,p2_y,p3_x,p3_y)
                if s >= 0 and s <= 1 and t >= 0 and t <= 1:
                        if fact > 0:
                            count_pos += 1
                        else:
                            count_neg += 1
                            
        return (count_pos,count_neg)
  
      
        
    def draw(self,screen):
        gui.draw_world(self,screen)
        """
        if not self.blind:
            for wall in self.walls:
                if "start" in wall.name:
                    col=(255,255,0)
                elif "end" in wall.name:
                    col=(0,255,255)
                else:
                    col=(0,0,255)

                for seg in wall.segments:
                    pg.draw.line(screen,col,(seg[0],seg[1]),(seg[2],seg[3]),6)
        
            col=(100,30,30)
            for t in self.trips:
                pg.draw.line(screen,col,t[0],t[1],2)
                
        
        
        for pod in self.pods:
            pod.draw(screen) #@IndentOk
    """
#        fontobject = pg.font.Font(None,20)
#        message=" Ticks: " + str(self.ticks)
#        screen.blit(fontobject.render(message, 1, (255,255,255)),
#                (20,20))
