import pygame as pg
from math import *

#
# 24/10/2010
#    set CarPod dangdt
#    modified slip to allow power slides (still very naff)

ang_thrust_max=0.5

white = (255,255,255)
red=(255,40,40)
huge=1e6
small=1e-6

def rotate_poly(poly,ang,pos):
    ret=[]
    for p1 in poly:
        x=p1[0]*cos(ang)+p1[1]*sin(ang)+pos.x
        y=-p1[0]*sin(ang)+p1[1]*cos(ang)+pos.y
        ret.append((x,y))
    return ret

def limit(x,min,max):
    if x > max:
        return 1
    elif x < min:
        return min
    else:
        return x


def read_points(fin):

    points=[]
    while True:
            line = fin.readline()
            if line[0] == '#':
                continue
                
            if line.isspace() or len(line)==0:
                return points

            toks = line.split(',')
            for tok in toks:
             #   print tok
                if len(tok) != 0 and not tok.isspace():
                    points.append(float(tok))


    #  t is normalized distance from p0 to p1
    #  s is normalized distance from p2 to p3
def intersect(p0_x,p0_y,p1_x,p1_y,p2_x,p2_y,p3_x,p3_y):
        s1_x = p1_x - p0_x
        s1_y = p1_y - p0_y
        s2_x = p3_x - p2_x
        s2_y = p3_y - p2_y

        fact = (-s2_x * s1_y + s1_x * s2_y)

        if fact == 0:
            return (huge,huge)

        s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / fact
        t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / fact

        return (s,t)


class Control:

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

    def __init__(self,pod):
        self.x=pod.x
        self.y=pod.y
        self.dxdt=pod.dxdt
        self.dydt=pod.dydt
        self.ang=pod.ang
        self.dangdt=pod.dangdt

 
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


        self.rect=pg.Rect(self.minX,self.minY,self.maxX-self.minX,self.maxY-self.minY)



class World:

    def __init__(self,fileName,pods):

        self.pods=pods
        self.walls=[]
        fin=open(fileName,"r")
        self.rect=pg.Rect(0,0,0,0)
        self.ticks=0
        self.blind=False
        while True:
            line = fin.readline()
            if len(line)==0:
                return
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

                # print "POD OK"

    def read_pod_pos(self,fin):
        line = fin.readline()
        linelist=line.split(',')

        x = float(linelist[0])
        y = float(linelist[1])
        
        for pod in self.pods:
            pod.x=x
            pod.y=y

    def find_closest_intersect(self,p0_x,p0_y,p1_x,p1_y):
        tMin=2
        wallMin=None
        for wall in self.walls:
            for seg in wall.segments:
                p2_x=seg[0]
                p2_y=seg[1]
                p3_x=seg[2]
                p3_y=seg[3]
                (s,t)=intersect(p0_x,p0_y,p1_x,p1_y,p2_x,p2_y,p3_x,p3_y)

                if t >= -small and t <= 1+small and s >= -small and s <= 1+small:
                    if t < tMin:
                        tMin=t
                        wallMin=wall

        return (tMin,wallMin)
        return



    def check_collide_with_wall(self,p0_x,p0_y,p1_x,p1_y):
        if p0_x==p1_x and p1_y==p0_y:
            return None

        for wall in self.walls:
            for seg in wall.segments:
                p2_x=seg[0]
                p2_y=seg[1]
                p3_x=seg[2]
                p3_y=seg[3]

                (s,t)=intersect(p0_x,p0_y,p1_x,p1_y,p2_x,p2_y,p3_x,p3_y)

                if s >= 0 and s <= 1 and t >= 0 and t <= 1:
                    return wall
        return None

    def step(self,dt):
        self.ticks += 1
        for pod in self.pods:
            pod.step(dt,self)
            pod.update_sensors(self)

    def draw(self,screen):
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

        for pod in self.pods:
            pod.draw(screen)

#        fontobject = pg.font.Font(None,20)
#        message=" Ticks: " + str(self.ticks)
#        screen.blit(fontobject.render(message, 1, (255,255,255)),
#                (20,20))

class Pod:
    pod_poly_ref=[(-10,-10),(0,20),(10,-10)]
    thrust_poly_ref=[(0,-10),(-2,-14),(0,-18),(2,-14)]
    left_poly_ref=[(-5,5),(-9,4),(-12,5),(-9,6)]
    right_poly_ref=[(5,5),(9,4),(12,5),(9,6)]

    def __init__(self,nSensor,sensorRange,brain,col):
        self.col=col
        self.ang=pi
        self.brain=brain
        self.dangdt=0
        self.x=0
        self.y=0
        self.dxdt=0
        self.dydt=0
        self.vel=0
        self.collide=False
        self.collide_count=0
        self.sensors=[]
        self.control=Control()
        for i in range(nSensor):
            ang_ref=i*pi*2/nSensor
            self.sensors.append(Sensor(ang_ref,sensorRange,"sensor"+str(i)))

    def update_sensors(self,world):
        for sensor in self.sensors:
            ang=sensor.ang_ref+self.ang
            sensor.ang=ang
            (s,wall)=world.find_closest_intersect(self.x,self.y,self.x+sensor.range*sin(ang),self.y+sensor.range*cos(ang))
            sensor.val=s*sensor.range
            if wall == None:
                sensor.wall=None
            else:
                sensor.wall=wall.name


    def draw(self,screen):
        self.draw_sensors(screen)
        self.draw_pod(screen)

    def draw_pod(self, screen):
        if self.collide:
            self.collide_count=100

        outline=rotate_poly(self.pod_poly_ref, self.ang, self)
        if self.collide_count>0:
            col=(255,100,100)
            self.collide_count -= 1
        else:
            col=self.col
        pg.draw.polygon(screen,col,outline)
        if self.control.up > 0.0:
            outline=rotate_poly(self.thrust_poly_ref, self.ang, self)
            pg.draw.polygon(screen,red,outline)
        if self.control.left > 0.0:
            outline=rotate_poly(self.left_poly_ref, self.ang, self)
            pg.draw.polygon(screen,red,outline)
        if self.control.right > 0.0:
            outline=rotate_poly(self.right_poly_ref, self.ang, self)
            pg.draw.polygon(screen,red,outline)


    def draw_sensors(self,screen):
        for sensor in self.sensors:
            wallName=sensor.wall
            if wallName== None:
                col=(10,10,10)
            elif "end" in wallName:
                col=(255,255,255)
            else:
                col=(70,70,70)

            dist=sensor.val
            
            p1=(self.x,self.y)
            p2=(self.x+dist*sin(sensor.ang),self.y+dist*cos(sensor.ang))
            pg.draw.line(screen,col,p1,p2,1)


class CarPod(Pod):
 
    def __init__(self,nSensor,sensorRange,brain,col):
        Pod.__init__(self,nSensor,sensorRange,brain,col)
        self.mass  = 20
        self.brake = 0
        self.steer_factor=.05
        self.thrust_max=200
        self.slip_thrust_max=200
        self.slip_speed_thresh=80
        self.slip_speed_max=200
        self.slip=0.0
        self.damp=.0001
        self.vel=0
       
    
    def step(self,dt,world):
        state=State(self)
        self.control=self.brain.process(self.sensors,state,dt)
        self.control.limit()

        slipThrust = (self.control.up-self.control.down)*self.slip*self.slip_thrust_max
        self.dxdt = self.dxdt*self.slip+(1.0-self.slip)*self.vel*sin(self.ang) +  sin(self.ang)*slipThrust*dt
        self.dydt = self.dydt*self.slip+(1.0-self.slip)*self.vel*cos(self.ang) +  cos(self.ang)*slipThrust*dt
        #self.dxdt = self.vel*sin(self.ang)
        #self.dydt = self.vel*cos(self.ang)

        xNext = self.x + self.dxdt*dt
        yNext = self.y + self.dydt*dt

        wall=world.check_collide_with_wall(self.x,self.y,xNext,yNext)
        
        ang_prev=self.ang
        
        if wall == None:
            self.x = xNext
            self.y = yNext
            if self.vel > 0:
                damp_fact=self.vel*self.vel*self.vel/abs(self.vel)
            else:
                damp_fact=0
                
            self.vel += (self.control.up-self.control.down)*self.thrust_max/self.mass-self.damp*damp_fact
            self.collide = False
            self.ang += 0.5*(2.0-self.slip)*(-self.control.right+self.control.left)*self.vel*self.steer_factor*dt + self.slip*self.dangdt*dt
            avel=abs(self.vel)
            if avel > self.slip_speed_max:
                self.slip=1
            elif avel > self.slip_speed_thresh:
                t=(avel-self.slip_speed_thresh)/(self.slip_speed_max-self.slip_speed_thresh)
                self.slip=t
            else:
                self.slip=0

        else:
            self.dydt = 0
            self.dxdt = 0
            self.vel  = 0
            self.collide = True
            self.ang += (-self.control.right+self.control.left)*self.vel*self.steer_factor*dt

        self.dangdt=(self.ang-ang_prev)/dt
 

class GravityPod(Pod):

    g = 2

    def __init__(self,nSensor,sensorRange,brain,col):
        Pod.__init__(self,nSensor,sensorRange,brain,col)
        self.mass=2
        self.inertia=.5     # angluar inertia
        self.thrustMax=20
        self.spinThrustMax=.11


    def step(self,dt,world):

        state=State(self)
        self.control=self.brain.process(self.sensors,state,dt)
        self.control.limit()

        xNext = self.x + self.dxdt*dt
        yNext = self.y + self.dydt*dt

        wall=world.check_collide_with_wall(self.x,self.y,xNext,yNext)
        if wall == None:
            self.x=xNext
            self.y=yNext
            thrust=self.thrustMax*self.control.up
            self.dydt += thrust*cos(self.ang)/self.mass+self.g
            self.dxdt += thrust*sin(self.ang)/self.mass
            self.collide=False
        else:
            self.dydt=0
            self.dxdt=0
            self.collide=True

        self.ang    += self.dangdt*dt
        self.dangdt += (-self.control.right+self.control.left)*self.spinThrustMax/self.inertia




class SimplePod(Pod):

    def __init__(self,nSensor,sensorRange,brain,col,stepSize=20):
        Pod.__init__(self,nSensor,sensorRange,brain,col)
        self.stepSize=stepSize

    def step(self,dt,world):
        state=State(self)
        self.control=self.brain.process(self.sensors,state,dt)
        self.control.limit()

    
        xNext = self.x + self.stepSize*(self.control.right - self.control.left)
        yNext = self.y + self.stepSize*(self.control.down - self.control.up)

        wall=world.check_collide_with_wall(self.x,self.y,xNext,yNext)
        if wall == None:
            self.x=xNext
            self.y=yNext
            self.collide=False
        else:
            self.collide=True


class Simulation:

    def __init__(self,world,dt):

        pg.init()
        self.dt=dt
        self.slowMotionFactor=1.0
        self.world = world
        dim_world = (self.world.rect.width+20, self.world.rect.height+20)
        self.frameskipfactor=1
        self.frameskipcount=1
        self.painter=None
        self.screen = pg.Surface(dim_world) #

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

    def run(self):

        clock = pg.time.Clock()
        frameRate=1.0/self.dt/self.slowMotionFactor

       # the event loop also loops the animation code
        while True:

            self.frameskipcount -= 1

            display= self.frameskipcount == 0 and self.frameskipfactor != 0

            if display:
                clock.tick(frameRate)
                self.frameskipcount=self.frameskipfactor

            pg.event.pump()
            keyinput = pg.key.get_pressed()

            if keyinput[pg.K_ESCAPE] or pg.event.peek(pg.QUIT):
                pg.display.quit()
                break
                # raise SystemExit


            self.world.step(self.dt)
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
            
