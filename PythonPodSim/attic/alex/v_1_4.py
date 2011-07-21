
import pygame as pg
from math import *
import csv



def lin_equation (angle, x,y):
    grad=sin(angle)/cos(angle)
    n=y- grad*x
    return Point (grad,n)

def intersection_point (grad1, grad2, n1, n2):

    if (grad2-grad1)==0:
        grads=0.0001
    else:
        grads=grad2-grad1
    x=int((n1-n2)/grads)
    y= int (grad1*x + n1)
    return Point (x,y)

def ccw(A,B,C):
	return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

def intersect(A,B,C,D): #checks whether the segments AB and CD intersect
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


def find_second_point_int(angle, x, y, drange):
   
    
    

    provX=cos(angle)*drange + x
    provY=sin(angle)*drange + y
    provX=int(provX)
    provY=int(provY)
    second_Point=Point(provX,provY)
   

    return second_Point


def create_walls():
    wallarray=[]
    csvReader = csv.reader(open('real_world.csv', 'rb'), delimiter=';')
    i=0
    j=0

    for row in csvReader:

        for column in row:
            if  i==0:
            
                valX= int(column)
                i=i+1
            
            elif i==1:
                valY= int(column)

                Point1=Point(valX, valY)
                i=i+1
            elif i==2:
                valX2=int(column)

                i=i+1
            elif i==3:
                valY2=int(column)
                #print "algo"
                Point2=Point(valX2, valY2)
                provName= "wall" + str(j)
                wallarray.append(wall(Point1,Point2, provName))
                Point1=Point2
            
                i=2
                j=j+1
    return wallarray
class dinput:
    def __init__(self):
        self.left=0
        self.right=0
        self.up=0
        self.down=0

    def limit(self):
        self.up=limit(self.up,0,1)
        self.right=limit(self.right,0,1)
        self.down=limit(self.down,0,1)
        self.left=limit(self.left,0,1)

class Sensor:
    def __init__(self, angle, srange, posx, posy, name): #xpos nad ypos will later disappear
        self.val=srange
        self.sangle=angle
        self.wall= False
        self.name= name
        
        self.sgrad=sin(angle)/cos(angle)
        self.snn= posx- self.sgrad * posy
        self.x=posx
        self.y=posy
        self.secondPoint= find_second_point_int (angle, posx, posy, srange)

        self.inwallnumber=0
class State:

    def __init__(self,pod):
        self.x=pod.posx
        self.y=pod.posy

        self.ang=pod.angle
        
        
        self.pod=pod
        
class carpod:
    def __init__(self,numberSensor,x,y,angles, brain):
        self.posx=x
        self.posy=y
        self.direction=brain
        self.angle=angles
        self.shift=0
        self.vel=0
        self.acceleration=0
        self.input=brain
        self.inputformat=dinput()
        self.sensors=[]
        
        for i in range(numberSensor):
            print i
            ang_ref=(i)*pi*2/numberSensor+self.angle
            self.sensors.append(Sensor(ang_ref,srange,self.posx, self.posy,"sensor"+str(i)))
            print "lle"
            
            #drawline(self.sensors[i].x, self.sensors[i].y, self.sensors[i].secondPoint.x, self.sensors[i].secondPoint.y, screen, (125,125,125))
            
            print"tttaa"
    def new_sensor(self,screen,wallarray):
        for i in range (numberSensor):
            colour=(200,200,200)
            ang=(i)*pi*2/numberSensor+ self.angle
            self.sensors[i].sangle=ang
            provEnd=find_second_point_int(ang,self.posx,self.posy,srange)
            self.sensors[i].x=self.posx
            self.sensors[i].y=self.posy
            flag=False
            for wall in wallarray:
                if intersect (Point(x,y), provEnd, wall.start, wall.end) == True:
                    eqSensor=lin_equation(ang, self.posx,self.posy)
                    self.sensors[i].secondPoint= intersection_point(eqSensor.x, wall.grad, eqSensor.y, wall.nn)
                    self.sensors[i].val = int(sqrt( (self.sensors[i].secondPoint.x - self.posx)**2 + (self.sensors[i].secondPoint.y - self.posy)**2 ))
                    self.sensors[i].wall=True

                    flag= True

            if flag==False:
                self.sensors[i].secondPoint= provEnd
                self.sensor[i].val = sRange
                self.sensor[i].wall=False
                
            drawline(self.posx,self.posy,self.sensors[i].secondPoint.x,self.sensors[i].secondPoint.y, screen, colour)

    def move(self):
## 
        print "A"  , self.input
        self.inputformat=brain.processX()
        print "B"

        
        if self.inputformat== None:
            return
        

        
        self.acceleration=self.acceleration*0.7 + self.inputformat.up*10 + self.inputformat.down*20
        if self.acceleration > 19:
            self.acceleration=19
    
            
        self.vel= self.acceleration* dt + self.vel
        if self.vel> 20:
            self.vel=20
        elif self.vel<0:
            self.vel=0
        self.angle=self.angle + pi/20* self.input.left - pi/20*self.input.right
        displacement=find_second_point_int (self.angle, x,y, self.vel)
        self.x=displacement.x
        self.y=displacement.y
    def drawPolygon(self,screen) :
        self.point1=find_second_point_int(self.angle, self.posx,self.posx, 40)

        self.point2=find_second_point_int(self.angle +pi/2, self.posx,self.posy, 10)
        self.point3=find_second_point_int(self.angle -pi/2, self.posx,self.posy, 10)
        pg.draw.polygon(screen,(250,0,0),((self.point1.x, self.point1.y), (self.point2.x, self.point2.y), (self.point3.x, self.point3.y)))

                        
                    

    



class wall:
    def __init__(self, startPoint, endPoint, wall_name):
        self.start= startPoint
        self.end= endPoint
        self.name=wall_name
        
        if (self.start.x-self.end.x)==0:
            self.grad=3000
        else:
            self.grad= (self.start.y - self.end.y)/(self.start.x-self.end.x)
        self.nn= self.start.y - self.grad * self.start.x
            

class Point:
    def __init__(self,x,y):
        self.y = y
        self.x=x

def drawline(startx, starty,endx, endy,screen, colour):
        pg.draw.line(screen,(0,250,0), (startx, starty), (endx, endy))
    

        
        

class framework:
    def __init__(self,pods):

        self.cars=pods
        
        self.walls=create_walls()
        
        
        
        self.rect=pg.Rect(0,0,0,0)
        self.ticks=0
        self.blind=False
        
    def step(self,screen):
        self.ticks += 1
        for carpod in self.cars:
            carpod.move()
            carpod.drawPolygon(screen)
            carpod.new_sensor(screen,self.walls)
    def drawWall(self,screen):
        for wall in self.walls:
            drawline(wall.start.x,wall.start.y,wall.end.x, wall.end.y, screen, (0,250,0))
                
    def drawCar(self,screen):
        for carpod in self.cars:
            print "yaaaaaaaaaaaaaa"
            carpod.drawPolygon(screen)#carpod.angle, carpod.posx, carpod.posx)
            
        
        
class real_time:

    def __init__(self,world,dt,admin=None):

        pg.init()
        self.admin=admin
        self.dt=dt
        
        self.environment = world
        self.dim_world = (700,700)
        self.frameskipfactor=1
        self.frameskipcount=1
        self.framework=world
        self.screen = pg.Surface(self.dim_world)
        world.drawWall(self.screen)
        world.drawCar(self.screen)
        
        

  

        self.display = pg.display.set_mode(self.dim_world)
        pg.display.set_caption('press escape to exit)')

    def run(self):

        clock = pg.time.Clock()
        
        self.tick_count=0
        
        self.screen.fill((50,50,50))
        self.framework.step
       # the event loop also loops the animation code
        while True:
            print "1"
            keyinput = pg.key.get_pressed()

            if keyinput[pg.K_ESCAPE] or pg.event.peek(pg.QUIT):
                pg.display.quit()
                break
            
            self.framework.step (self.screen)
            pg.display.flip()




            
class CursorControl:
    def __init__(self):
        self.up=0
        self.down=0
        self.left=0
        self.right=0
  
    def processX(self):
        control=dinput()
        self.up=0
        self.down=0
        self.left=0
        self.right=0

        
        keyinput = pg.key.get_pressed()

        if keyinput[pg.K_LEFT]:
            control.left=.4

        if keyinput[pg.K_RIGHT]:
            control.right=.4

        if keyinput[pg.K_UP]:
            control.up=1

        if keyinput[pg.K_DOWN]:
            control.down=1
        return control



brain=CursorControl()





initialx=50
initialy=650
noSensors=10
initialAngle=0
dt=0.1
numberSensor=10
srange=40
#brain=CursorControl
#Reader = csv.reader(open('world.csv', 'rb'), delimiter=';')

podOb=carpod(noSensors,initialx, initialy,initialAngle, brain)
podObs=[podOb]
Environment=framework(podObs)
sim=real_time(Environment,dt)
sim.run()





























# Initialize the drawing window.
pg.init ()

#draw.polygon(screen,(1,160,5),((0,0), (0, 100), (100,0)))
posi=Point(60,90)
srange=30
x=60
y= 90
angles=0
print cos(angles)
print sin (angles)



#trompa=drawcar(angles,x,y)
#trompa.drawpolygon(angles, posi.x, posi.y)

#ferrari=carpod(10,x,y,0, angles)

#print trompa.point1.x, trompa.point1.y
#print trompa.point2.x, trompa.point2.y
#print trompa.point3.x, trompa.point3.y
#print trompa.point1.y
#print trompa.point2.y
#print trompa.point3.y

# Show anything.

        
    
