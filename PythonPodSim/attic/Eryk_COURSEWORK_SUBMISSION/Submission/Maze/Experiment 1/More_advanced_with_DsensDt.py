from simulation import *
import pygame 
from random import  *

#
#    Manual drive a car around a track
#
starty = 0
startx = 0
collision_no = 0


def init(state):

       
    
       
        global startx, starty, previous_sensor_value,previous_diff,avg,sens17

        startx = state.x
        starty = state.y
        sens17 = [0,0]


         
        
        
        
        return 
    
    
def toString(sensors,state,control):
    
    ret= str("Input,")+str(state.dxdt)+","+ str(state.dydt) + "," + str(state.ang)+ ","
    ret= ret
    for s in sensors:
        ret = ret + str(s.val) + ","
    
    
    ret+= str("Control,") + str(control.up)+"," +str(control.down)+","+ str(control.left)+ ","+ str(control.right) +" \n"
        
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
            #optimal 241 spped and accelereation1.18
            Front_sensor_Gain=1.51*sensor[0].val
            if Front_sensor_Gain>225:
                Front_sensor_Gain=225
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
