from simulation import *
import pygame 

#
#    Manual drive a car around a track
#
starty = 0
startx = 0
collision_no = 0

def init(state):

       
        
        
       
        global startx, starty
        startx = state.x
        starty = state.y
        return 
    
def read_data(file_name):
    ftd=open(file_name,"r")
    cnt=[]
    cnt4=[]
    while True: 
        line = ftd.readline()
        #print line
        if line.isspace() or len(line)==0:
            return cnt
        toks = line.split(',')
        for tok in toks:
           #print tok
           if len(tok) != 0 and not tok.isspace() :
                cnt4.append(float(tok))
                if len(cnt4)==4:
                    cnt.append(cnt4)
                    cnt4=[]

                    
                

class CarControl:    
     
    
    def process(self,sensor,state,dt):
        
        a=(state.pod.pos_trips-state.pod.neg_trips)
        #print beacon[a]
        for i in range(4):
            print(beacon[a][i])
        
        print
        control=Control()
        keyinput = pygame.key.get_pressed()

        if keyinput[pg.K_LEFT]:
            control.left=1

        if keyinput[pg.K_RIGHT]:
            control.right=1

        if keyinput[pg.K_UP]:
            control.up=1

        if keyinput[pg.K_DOWN]:
            control.down=1
            
       
        return control


    
beacon = read_data("beacons")
print beacon

dt          = 0.1
brain       = CarControl()
nSensors    = 40
sensorRange = 2000
pod         = CarPod(nSensors,sensorRange,brain,(150,0,255))
#pod         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
pods        = [pod]
world       = World("trip_world.txt",pods)
sim         = Simulation(world,dt)

#uncomment the next line to hide the walls.


#sim.world.blind=True
#sim.frameskipfactor=10


sim.run()
