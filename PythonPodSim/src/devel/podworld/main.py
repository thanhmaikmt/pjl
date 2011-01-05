from agent import *
from world import  *
from painter import *
from pool import  *
from admin import  *
from simulation import *

#run="carNN"
#run="gravityNN"
run="carNN"

if run == "carNN":
    from NNBrainPlug import *
    import carplug 

    podPlug=carplug.CarPlug()
    brainPlug=BrainPlug(carplug.layerSizes)
     
    class CarAngleGoal:
        
        def __init__(self,ang):
            self.ang=ang
            
    goals=[CarAngleGoal(.0),CarAngleGoal(-.5),CarAngleGoal(0.5)]
    
     
elif run == "gravityNN":
    
    from NNBrainPlug import *
    import gravityplug 

    podPlug=gravityplug.GravityPlug()
    brainPlug=BrainPlug(gravityplug.layerSizes)
   
   

elif run ==  "carParam":
    
    import carparam
    podPlug=carparam.CarParamPlug()
    brainPlug=carparam.ParamBrainPlug()
    



###  START OF PROGRAM
dt    = .1
world = World(podPlug.WORLD_FILE,dt)


pool  = Pool(world,brainPlug,goals)    #  create a pool for fittest networks
    
agents=[]        #  pods on the circuits
#pool = None

POP_SIZE=10

for i in range(POP_SIZE):     # create initial population on the circuit
    brain=brainPlug.createBrain()
    pod = podPlug.createInitialPod(i,brain)
    agents.append(Agent(pod))


admin = Admin()
sim   = Simulation(world,agents,podPlug,pool,admin,podPlug.RUN_NAME)

# register the painter to display stuff
sim.painter = Painter(sim,podPlug.RUN_NAME)

# go go go  ..........
sim.run()