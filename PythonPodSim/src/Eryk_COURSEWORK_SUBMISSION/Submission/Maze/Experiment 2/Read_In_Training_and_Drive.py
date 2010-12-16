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
    while True: 
        line = ftd.readline()
        #print line
        if line.isspace() or len(line)==0:
                print cnt
                return cnt
        
        
                
        if line.isspace() or len(line)==0:
           return points
        toks = line.split(',')
        cont=0
        for tok in toks:
           #print tok
           if len(tok) != 0 and not tok.isspace() :
                if cont == 1:
                   cnt.append(float(tok))
                if tok == "Control":
                   cont=1
                   #print "control found"
                    
                

class CarControl:    
     
    
    def process(self,sensor,state,dt):
        
        if starty == 0 and startx ==0:
           init(state)
                
        control=Control()
        print "Position"
        print "x: "+str(state.x)+ "  y: "+str(state.y)+  " Ang: "+str(state.ang)+ "\n"
        print "Speed"
        print  "x: "+str(state.dxdt)+ " y: "+str(state.dydt)+" Ang: "+str(state.dangdt)+ "\n"
        print "Sensors"
        print "N: val:"+str(int(sensor[0].val))+" ang:"+str(sensor[0].ang), " wall:"+str(sensor[0].wall)
        print "S: val:"+str(int(sensor[20].val))+" ang:"+str(sensor[20].ang), " wall:"+str(sensor[20].wall)
        print "W: val:"+str(int(sensor[30].val))+" ang:"+str(sensor[30].ang), " wall:"+str(sensor[30].wall)
        print "E: val:"+str(int(sensor[10].val))+" ang:"+str(sensor[10].ang), " wall:"+str(sensor[10].wall), "\n"
        
        
       
            
        keyinput = pygame.key.get_pressed()

        if keyinput[pg.K_LEFT]:
            control.left=1

        if keyinput[pg.K_RIGHT]:
            control.right=1

        if keyinput[pg.K_UP]:
            control.up=1

        if keyinput[pg.K_DOWN]:
            control.down=1
            
        control.up=data.pop(0)
        control.down=data.pop(0)
        control.left=data.pop(0)
        control.right=data.pop(0)
             
        print "UP: "+str(control.up) + " DN: "+str(control.down) +" L: "+str(control.left) +" R: "+str(control.right)
       
        if pod.collide==True:
            pod.y=starty
            pod.x=startx
            pod.ang=pi
            pod.vel=0
            global collision_no
            collision_no+=1
            print "\n\ncollision #no",str(collision_no),startx,starty,"\n\n"
        
       
        return control

print "1 - Pre Procesed TD"
print "2 - Post Processed TD"
var = raw_input("Enter 1 or 2: ")
print "you entered ", var

if var=="1":
    data = read_data("Training.csv")
else:
    data = read_data("Training_Post_process.csv")

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
