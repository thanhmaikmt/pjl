'''
Created on 21 Dec 2010

@author: pjl
'''
from config import *

if NUMPY:
    import numpy
    
from math import *
from util import *
import gui

ang_thrust_max=0.5
white = (255,255,255)
red=(255,40,40)
small=1e-6


    
class Control:
    " A control message "
    def __init__(self):
        self.left=0
        self.right=0
        self.up=0
        self.down=0

    def limit(self):
        " limit all values to 0-1 range "
        self.up=limit(self.up,0,1)
        self.right=limit(self.right,0,1)
        self.down=limit(self.down,0,1)
        self.left=limit(self.left,0,1)

class Sensor:
    """  
        ang_ref:  anticlockwise angle from forward 
        range: 
        name:
    """
           
    def __init__(self,ang_ref,range,name):
       
        
        self.ang_ref=ang_ref
        self.ang=ang_ref
        self.range=range
        self.val=0
        # self.val=0
        self.wall="None"
        self.name=name

    def to_string(self):
        return str(int(self.val*self.range))


class State: 
    def __repr__(self):
        txt=""
        for attr, value in self.__dict__.iteritems():
            txt+=str(attr)+ " "+ str(value)+"\n" 
     
        return txt
        
class Pod:
    """ Base class for all pods """
    
    pod_poly_ref=[(-10,-10),(0,20),(10,-10)]
    thrust_poly_ref=[(0,-10),(-2,-14),(0,-18),(2,-14)]
    left_poly_ref=[(-5,5),(-9,4),(-12,5),(-9,6)]
    right_poly_ref=[(5,5),(9,4),(12,5),(9,6)]


    def __init__(self,col):
       
        self.message="init"
        self.control=Control()
        self.sensors=[]
        self.base_init()    
        self.col=col
        self.base_init()
            
    def addSensors(self,sensors): 
        self.sensors.extend(sensors)
        if NUMPY:
            self.sensor_x1=len(sensors)*[0.0]
            self.sensor_y1=len(sensors)*[0.0]
            self.sensor_x2=len(sensors)*[0.0]
            self.sensor_y2=len(sensors)*[0.0]
                    
    def setController(self,controller):
       self.controller=controller
             
    def base_init(self):
        self.state=State() 
        self.state.ang=pi
        self.state.dangdt=0.0
        self.state.x=0.0
        self.state.y=0.0
        self.state.dxdt=0.0
        self.state.dydt=0.0
        self.state.vel=0.0
        self.state.collide=False
        self.state.collide_count=0
        self.state.age=0.0
        self.state.pos_trips=0
        self.state.neg_trips=0
        self.state.distance_travelled=0.0
     
    def update_sensors_todo_fixme(self):
        world=self.world
        state=self.state
        
        cnt=0
        for sensor in self.sensors:
            ang=sensor.ang_ref+state.ang
            sensor.ang=ang
            self.sensor_x1[cnt]=state.x
            self.sensor_y1[cnt]=state.y
            self.sensor_x2[cnt]=state.x+sensor.range*sin(ang)
            self.sensor_y1[cnt]=state.y+sensor.range*cos(ang)
            cnt+=1
            
        
        (s,wall)=world.find_closest_intersect2_vec(self.sensor_x1,self.sensor_y1,self.sensor_x2,self.sensor_y2)
        
        cnt=0
        for sensor in self.sensors:
            sensor.val=s[cnt]*sensor.range
            if wall[cnt] == None:
                sensor.wall=None
            else:
                sensor.wall=wall[cnt].name 
        
    def update_sensors(self):
        world=self.world
        state=self.state
        
        
        for sensor in self.sensors:
            ang=sensor.ang_ref+state.ang
            sensor.ang=ang
            (s,wall)=world.find_closest_intersect(state.x,state.y,state.x+sensor.range*sin(ang),state.y+sensor.range*cos(ang))

            sensor.val=s*sensor.range
            if wall == None:
                sensor.wall=None
            else:
                sensor.wall=wall.name


    def draw(self,screen):
        gui.draw_sensors(self,screen)
        gui.draw_pod(self,screen)

 

class CarPod(Pod):
 
    def __init__(self,col=(255,0,0)):
        Pod.__init__(self,col)
        self.init()
    
    def setColour(self,col):
        self.col=col
        
    def init(self):
        self.base_init()
        self.mass  = 10.
        self.brake = 0.
        self.steer_factor=.05
        self.thrust_max=200.
        self.slip_thrust_max=200.
        self.slip_speed_thresh=80.
        self.slip_speed_max=200
        self.slip=0.0
        self.damp=.0001
        #self.vel=0.0
        self.fuel=0.0
        self.state.distance_travelled=0.0
   
        
        
    def step(self):
        world=self.world
        dt=world.dt
        state=self.state
        self.control=self.controller.process(self,dt)
        if self.control == None:
            return
        
        self.fuel -= self.control.up*dt
        self.state.age += dt
        
        self.control.limit()

        slipThrust = (self.control.up-self.control.down)*self.slip*self.slip_thrust_max
        state.dxdt = state.dxdt*self.slip+(1.0-self.slip)*state.vel*sin(state.ang) +  sin(state.ang)*slipThrust*dt
        state.dydt = state.dydt*self.slip+(1.0-self.slip)*state.vel*cos(state.ang) +  cos(state.ang)*slipThrust*dt
        #self.dxdt = self.vel*sin(self.ang)
        #self.dydt = self.vel*cos(self.ang)

        xNext = state.x + state.dxdt*dt
        yNext = state.y + state.dydt*dt

        wall,seg_pos=world.check_collide_with_wall(state.x,state.y,xNext,yNext)
        
        ang_prev=state.ang
        
        if wall == None:

            (p,n)=world.count_trips(state.x,state.y,xNext,yNext)
            state.pos_trips += p
            state.neg_trips += n
        
            #nprint self.pos_trips,self.neg_trips
            
            state.x = xNext
            state.y = yNext
            if state.vel > 0:
                damp_fact=state.vel*state.vel*state.vel/abs(state.vel)
            else:
                damp_fact=0
                
            state.vel += (self.control.up-self.control.down)*self.thrust_max/self.mass-self.damp*damp_fact
            state.collide = False
            state.ang += 0.5*(2.0-self.slip)*(-self.control.right+self.control.left)*state.vel*self.steer_factor*dt + self.slip*state.dangdt*dt
            avel=abs(state.vel)
            if avel > self.slip_speed_max:
                self.slip=1
            elif avel > self.slip_speed_thresh:
                t=(avel-self.slip_speed_thresh)/(self.slip_speed_max-self.slip_speed_thresh)
                self.slip=t
            else:
                self.slip=0

            

        else:
            state.seg_pos=seg_pos
            state.dydt = 0
            state.dxdt = 0
            state.vel  = 0
            state.collide = True
            state.ang += (-self.control.right+self.control.left)*state.vel*self.steer_factor*dt

        self.state.distance_travelled += sqrt(state.dxdt**2+state.dydt**2)*dt
        state.dangdt=(state.ang-ang_prev)/dt
 

class GravityPod(Pod):

    g = 2

    def __init__(self,sensors,plug,col):
        Pod.__init__(self,sensors,plug,col)
        self.init()
     
    def init(self):
        self.base_init()
        self.mass=2
        self.inertia=.5     # angluar inertia
        self.thrustMax=20
        self.spinThrustMax=.11
        #self.vel=0.0
        self.fuel=0.0
        self.distanceTravelled=0.0
        #self.age=0.0
        #self.pos_trips=0
        #self.neg_trips=0
        #self.collide=False

    def step(self):

        
        world=self.world
        dt=world.dt
        
        # state=State(self)
        self.control=self.controller.process(self,dt)
        if self.control == None:
            return
        
        self.control.limit()
        
        state=self.state
        
        state.age += dt
        xNext = state.x + state.dxdt*dt
        yNext = state.y + state.dydt*dt

        wall,dmy=world.check_collide_with_wall(state.x,state.y,xNext,yNext)
        if wall == None:
            (p,n)=world.count_trips(state.x,state.y,xNext,yNext)
            state.pos_trips += p
            state.neg_trips += n
        
            state.x=xNext
            state.y=yNext
            thrust=self.thrustMax*self.control.up
            state.dydt += thrust*cos(state.ang)/self.mass+self.g
            state.dxdt += thrust*sin(state.ang)/self.mass
            state.collide=False
        else:
            state.dydt=0
            state.dxdt=0
            state.collide=True

        state.ang    += state.dangdt*dt
        state.dangdt += (-self.control.right+self.control.left)*self.spinThrustMax/self.inertia




class SimplePod(Pod):

    def __init__(self,nSensor,sensorRange,col,stepSize=20):
        Pod.__init__(self,nSensor,sensorRange,col)
        self.stepSize=stepSize

    def step(self,dt,world):
        state=State(self)
        self.control=self.controller.process(self.sensors,state,dt)
        self.control.limit()

    
        xNext = state.x + self.stepSize*(self.control.right - self.control.left)
        yNext = state.y + self.stepSize*(self.control.down - self.control.up)

        wall=world.check_collide_with_wall(state.x,state.y,xNext,yNext)
        if wall == None:
            state.x=xNext
            state.y=yNext
            state.collide=False
        else:
            state.collide=True
