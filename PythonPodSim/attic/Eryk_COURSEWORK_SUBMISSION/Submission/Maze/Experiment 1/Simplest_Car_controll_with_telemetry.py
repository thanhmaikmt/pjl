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
        
        
       
            
        """
        sum_left=0
        sum_right=0
        i=1
        while i < nSensors/2:
            sum_left+=sensor[i].val
            i+=i
        i=nSensors/2
        while i < nSensors:
            sum_right+=sensor[i].val
            i+=i
        print sum_left
        print sum_right
        """
        
        control.up=0.1
        
        if sensor[0].val < 70:
            if sensor[10].val>sensor[30].val:
                control.left=1
            else:
                control.right=1
                
        
             
        print "UP: "+str(control.up) + " DN: "+str(control.down) +" L: "+str(control.left) +" R: "+str(control.right)
       
        if pod.collide==True:
            pod.y=starty
            pod.x=startx
            pod.ang=pi
            pod.vel=0
            global collision_no
            collision_no+=1
            print "\n\ncollision #no",str(collision_no),startx,starty,"\n\n"
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



dt          = 0.1
brain       = CarControl()
nSensors    = 40
sensorRange = 2000
pod         = CarPod(nSensors,sensorRange,brain,(150,0,255))
#pod         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
pods        = [pod]
world       = World("world.txt",pods)
sim         = Simulation(world,dt)

#uncomment the next line to hide the walls.


#sim.world.blind=True
#sim.frameskipfactor=10


sim.run()
