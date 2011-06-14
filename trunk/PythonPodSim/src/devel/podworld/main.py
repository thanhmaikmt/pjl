from world import  *
from agent import *
from painter import *
from pool import  *
from admin import  *
from simulation import *

run="carNN"
#run="gravityNN"
#run="carNN"

class CarAngleGoal:
        
        def __init__(self,ang):
            self.ang=ang
            
        def to_string(self):
            return str(self.ang)

if run == "carNN":
    from NNBrainPlug import *
    import carplug 

    podPlug=carplug.CarPlug()
    brainPlug=BrainPlug(carplug.layerSizes)
     
   
            
    goals=[CarAngleGoal(.0),CarAngleGoal(-.5),CarAngleGoal(0.5)]
    
     
elif run == "gravityNN":
    
    from NNBrainPlug import *
    import gravityplug 

    podPlug=gravityplug.GravityPlug()
    brainPlug=BrainPlug(gravityplug.layerSizes)
    goals=[CarAngleGoal(-.5),CarAngleGoal(0.5)]
   

elif run ==  "carParam":
    
    import carparam
    podPlug=carparam.CarParamPlug()
    brainPlug=carparam.ParamBrainPlug()
    goals=[CarAngleGoal(.0),CarAngleGoal(-.5),CarAngleGoal(0.5)]



pool  = Pool_Mino(50,brainPlug,goals)    #  create a pool for fittest networks
    
pods=[]        #  pods on the circuits
#pool = None

POP_SIZE=10

for i in range(POP_SIZE):     # create initial population on the circuit
    brain=pool.create_new_brain()

    pod = podPlug.createInitialPod(i,brain)
    pods.append(pod)

###  START OF PROGRAM
reaperPlug=podPlug
dt    = .1
world = World(podPlug.WORLD_FILE,dt,pods,reaperPlug,pool)

admin = Admin()
sim   = Simulation(world,podPlug.RUN_NAME,dt)
sim.setAdmin(admin)

# register the painter to display stuff
sim.painter = Painter(sim,podPlug.RUN_NAME)

# go go go  ..........
sim.run()