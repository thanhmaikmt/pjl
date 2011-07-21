from simulation import *
import pygame 
from random import  *

#
#    Manual drive a car around a track
#
starty = 0
startx = 0
collision_no = 0
c1=0
c2=0

def init(state):

       
    
       
        global startx, starty, previous_sensor_value,previous_diff,avg,sens17

        startx = state.x
        starty = state.y
        previous_sensor_value=[0,0,0,0,0,0,0,0]
        previous_diff=[0]
        avg=[0,0,0,0,0,0,0,0]
        sens17 = [0,0]


         
        
        
        
        return 
    
    
def toString(sensors,state,control):
    """
    ret= str("Input,")+str(state.dxdt)+","+ str(state.dydt) + "," + str(state.ang)+ ","
    ret= ret
    for s in sensors:
        ret = ret + str(s.val) + ","
    """
    
    ret= str("Control,") + str(control.up)+"," +str(control.down)+","+ str(control.left)+ ","+ str(control.right) +" \n"
        
    return ret   

class CarControl:

    def calc_fitness(self,state):
      
        # encourage them to go fast once they get round the path
        if state.pod.pos_trips == N_TRIP:
            fitness = N_TRIP + MAX_AGE-state.pod.age
        else:    
        # just count the trip wires we have passed        
            fitness = state.pod.pos_trips-state.pod.neg_trips
        
        return fitness   
     
    
    def process(self,sensor,state,dt):
        
        if starty == 0 and startx ==0:
           init(state)
           global c1,c2
                
        control=Control()
        sensdt=[]
        land = False
        
        distFromStart = sqrt((state.x-startx)**2+(starty-state.y)**2)
        
        keyinput = pygame.key.get_pressed()

        global training

        if keyinput[pg.K_t]:
            training = not training
           
            if not training:
                print "closing file "
                file.close()
                return
        
        


            
    
        
       
        if pod.collide==True or keyinput[pg.K_q]:
            pod.y=starty
            pod.x=startx
            pod.ang=pi+random()-0.5
            pod.vel= 0
            pod.distanceTravelled=0
            global collision_no
            collision_no+=1
            print "\n\ncollision #no",str(collision_no),startx,starty,"\n\n"
            
            
        if land == False:
            Front_sensor_Gain=1.40*sensor[0].val
            if Front_sensor_Gain>230:
                Front_sensor_Gain=230
            Vellocity_corection=(Front_sensor_Gain/(abs(pod.vel)+0.01)) - 1
            
            if Vellocity_corection > 0:
                if Vellocity_corection>1:
                    Vellocity_corection=1
                control.up = Vellocity_corection
            else:
                if abs(Vellocity_corection)>1:
                    Vellocity_corection=1
                control.down = abs(Vellocity_corection)
                
            Sensor_diffrence=(sensor[1].val+sensor[2].val)-(sensor[7].val+sensor[6].val)
            Turning_correction=-0.0091*sensor[0].val+1.1818
            #y=-0.00003*(sensor[0].val)**2-0.0018*sensor[0].val+ 1.01
            #y = 0.000001*sensor[0].val**3 - 0.0002*sensor[0].val**2 - 0.0027*sensor[0].val + 1.0179
            if Turning_correction<0:
                Turning_correction = 0
            control.down=Turning_correction

            if Sensor_diffrence>0:
                #control.left=abs((diff/100)**2/70)+y
                control.left= abs(0.0009*Sensor_diffrence)+Turning_correction
                #control.left=0.0396*exp(0.0051*abs(diff))+y
            else:
                #control.right=abs((diff/100)**2/70)+y
                control.right = abs(0.0009*Sensor_diffrence)+Turning_correction
                #control.right=0.0396*exp(0.0051*abs(diff))+y

            dsensdt7=(sensor[7].val - sens17.pop())
            dsensdt1=(sensor[1].val - sens17.pop())
            
            sens17.append(sensor[1].val)
            sens17.append(sensor[7].val)

            
            if dsensdt1>10:
                control.left+=dsensdt1/300.0

            if dsensdt7>10:
                control.right+=dsensdt7/300.0
            
            
            
            white_pod=self.calc_fitness(state)
            print "fit" +str(white_pod)
            
            if training:
                file.write(toString(sensor,state,control))
                
                
                
                
        else:
            print "Landing"
            #to be continuted
            
                
        
        return control           

class CarCursor:

    def calc_fitness(self,state):
      
        # encourage them to go fast once they get round the path
        if state.pod.pos_trips == N_TRIP:
            fitness = N_TRIP + MAX_AGE-state.pod.age
        else:    
        # just count the trip wires we have passed        
            fitness = state.pod.pos_trips-state.pod.neg_trips
        
        return fitness   
    
    
    def process(self,sensor,state,dt):
        
        if starty == 0 and startx ==0:
           init(state)
           global c1,c2
                
        control=Control()
        sensdt=[]
        land = False
        
        distFromStart = sqrt((state.x-startx)**2+(starty-state.y)**2)
        
        print "Position"
        print "x: "+str(state.x)+ "  y: "+str(state.y)+ " Ang: "+str(state.ang)+ "\n"
        print "Speed"
        print  "x: "+str(state.dxdt)+ " y: "+str(state.dydt)+ " vel: "+str(pod.vel)+" Ang: "+str(state.dangdt)+ "\n"
        print "Distance"
        print "s travelled: " +str(pod.distanceTravelled)+ " s from origin: "+ str(distFromStart) + "\n"
        print "Sensors"
        No=-1
        
        for s in sensor:   
            No+=1
            change = previous_sensor_value.pop()
            change = s.val-change
            sensdt.append(change)
            print str(No)+": val:"+str(int(s.val))+" ang:"+str(round(s.ang,3)), " wall:"+str(s.wall), "change: " +str(change)
            
            if s.wall == "end":
                print "landing platform"
                #land = True
            
        for s in sensor: 
            previous_sensor_value.append(float(s.val))
            
        previous_sensor_value.reverse()
                
       # print "N: val:"+str(int(sensor[0].val))+" ang:"+str(sensor[0].ang), " wall:"+str(sensor[0].wall)
       # print "NE: val:"+str(int(sensor[1].val))+" ang:"+str(sensor[1].ang), " wall:"+str(sensor[1].wall)
       # print "E: val:"+str(int(sensor[2].val))+" ang:"+str(sensor[2].ang), " wall:"+str(sensor[2].wall)
       # print "ES: val:"+str(int(sensor[3].val))+" ang:"+str(sensor[3].ang), " wall:"+str(sensor[3].wall)
       # print "S: val:"+str(int(sensor[4].val))+" ang:"+str(sensor[4].ang), " wall:"+str(sensor[4].wall)
       # print "SW: val:"+str(int(sensor[5].val))+" ang:"+str(sensor[5].ang), " wall:"+str(sensor[5].wall)
       # print "W: val:"+str(int(sensor[6].val))+" ang:"+str(sensor[6].ang), " wall:"+str(sensor[6].wall)
       # print "WN: val:"+str(int(sensor[7].val))+" ang:"+str(sensor[7].ang), " wall:"+str(sensor[7].wall), "\n"
        
        
        
       
        if pod.collide==True:
            pod.y=starty
            pod.x=startx
            pod.ang=pi
            pod.vel= 0
            pod.distanceTravelled=0
            global collision_no
            collision_no+=1
            print "\n\ncollision #no",str(collision_no),startx,starty,"\n\n"
            
            
        if land == False:

            control=Control()
            keyinput = pygame.key.get_pressed()

           

        
            diff=(sensor[1].val+sensor[2].val)-(sensor[7].val+sensor[6].val)
            print "Diff:       " +str(diff)
            
            grad=previous_diff.pop()-diff
            if abs(grad)== abs(diff):
                grad=0
            change=grad/(diff+0.001)
            avg.append(change)
            (sum(avg, 0.00) / len(avg))
            if len(avg)>10:
                avg.pop(0)
            av=(sum(avg, 0.00) / len(avg))
            
            print "Change in diff: "+str(grad)+ " %:" +str(change)+ "av: " +str(av)
            previous_diff.append(diff)
            
    
            y2=(sensor[7].val - sens17.pop())
            y1=(sensor[1].val - sens17.pop())
            
            
            if y1>50:
                c1=0.5
                
            
            if y2>50:
                c2=0.5
                
            if pod.vel==0:
                c1=0
                c2=0
            
                
            sens17.append(sensor[1].val)
            sens17.append(sensor[7].val)
            
            
            
            if c1<0:
                c1=0
            control.left=c1
            c1=c1-0.05
                

            if c2<0:
                c2=0
            control.right=c2
            c2= c2-0.05
                
                
            print "sens1: " +str(c1)
            print "sens7: " +str(c2)
            
            white_pod=self.calc_fitness(state)
            print "Fitness:" +str(white_pod)
            
            
            
            if keyinput[pg.K_LEFT]:
                control.left=.7

            if keyinput[pg.K_RIGHT]:
                control.right=.7

            if keyinput[pg.K_UP]:
                control.up=1
            
            if keyinput[pg.K_DOWN]:
                control.down=1
                
                
                
                
        else:
            print "Landing"
            #to be continuted
            
                
            
        print "UP: "+str(control.up) + " DN: "+str(control.down) +" L: "+str(control.left) +" R: "+str(control.right)
        
        return control

training=True
if training:
    file = open("Training.csv","w")

dt          = 0.1
brain       = CarControl()
brain1      = CarCursor()
nSensors    = 8
sensorRange = 2000
pod         = CarPod(nSensors,sensorRange,brain,(150,0,255))
pod1         = CarPod(nSensors,sensorRange,brain1,(255,0,255))
#pod         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
pods        = [pod]
world       = World("trip_world.txt",pods)
N_TRIP      = 21 
MAX_AGE     = 80 
sim         = Simulation(world,dt)

#uncomment the next line to hide the walls.


#sim.world.blind=True
#sim.frameskipfactor=10


sim.run()
