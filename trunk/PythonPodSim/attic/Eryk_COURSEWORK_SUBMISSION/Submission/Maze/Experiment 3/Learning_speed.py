from simulation import *
import pygame 
from fontmanager import  *

#
#    Manual drive a car around a track
#
starty = 0
startx = 0
startang = 0
reset = False
sens17 = []
itter=0
fitness=[80]
speed_array=[220]
acceleration_array=[1.2]
c1=0
c2=0

def init(state):

       
    
       
        global startx, starty, startang, sens17

        startx = state.x
        starty = state.y
        startang = pod.ang
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
           global c1,c2, itter, fitness, speed, acceleration, reset
           speed=220
           acceleration=1.2
                
        control=Control()
        
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
            
            
        if keyinput[pg.K_q]:
            reset=True
        
        if keyinput[pg.K_p]:
            sim.frameskipfactor = sim.frameskipfactor+1
            print "skip factor" ,sim.frameskipfactor
            
        if keyinput[pg.K_l]:
            sim.frameskipfactor = max(1,sim.frameskipfactor-1)
            print "skip factor" ,sim.frameskipfactor
            


        white_pod=self.calc_fitness(state)
       
        if pod.collide==True or reset==True:
            
            max_itter=10000
            
            reset=False
            fitness.append(white_pod)
            #print fitness
            best=fitness.index(max(fitness))
            speed_array.append(speed)
            #print speed_array
            acceleration_array.append(acceleration)
            #print acceleration_array
            itter+=1
            acceleration+=0.01
            if fitness[(itter)]<= 10:
                speed=speed+1
                acceleration=acceleration_array[best]-0.5
                
            if max_itter<=0:
                speed=speed_array[best]
                accelaration=acceleration_array[best]
                print "Max Iteration Reached"
                
            print
            print "Current speed: "+str(speed)+ " a: " +str(acceleration)+ " fitness: " +str(white_pod)
            print "Best so far, speed: " +str(speed_array[best]) + " acc: " +str(acceleration_array[best])+ " fitness: " +str(fitness[best])
            
           
            
            pod.y=starty
            pod.x=startx
            pod.ang=startang
            pod.vel= 0
            pod.distanceTravelled=0
            white_pod=0
            pod.age=0
            pod.pos_trips=0
            pod.neg_trips=0
            
           
            
            
            
        if land == False:
            Front_sensor_Gain=acceleration*sensor[0].val
            if Front_sensor_Gain>speed:
                Front_sensor_Gain=speed
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
            if white_pod>21 or pod.age>35:
                reset=True
            
            
            if training:
                file.write(toString(sensor,state,control))
                
                
                
            
        
                
        
        return control           



training=False
if training:
    file = open("Training.csv","w")

dt          = 0.1
brain       = CarControl()
nSensors    = 8
sensorRange = 2000
pod         = CarPod(nSensors,sensorRange,brain,(150,0,255))
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
