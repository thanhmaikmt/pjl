from world import  *
from agent import *
from painter import *

from admin import  *
from simulation import *
# import cprofile




run="carNN"
#run="gravityNN"
#run="carNN"



if run == "carNN":
 
    import carplug 

    podPlug=carplug.CarPlug()
   
    
     
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





pods=podPlug.createInitialPods()
###  START OF PROGRAM
reaperPlug=podPlug.getReaper()

dt    = .1

world = World(podPlug.WORLD_FILE,dt,pods,reaperPlug)
world.pool=podPlug.pool

admin = Admin()
sim   = Simulation(world,podPlug.RUN_NAME)
sim.setAdmin(admin)

# register the painter to display stuff
sim.painter = Painter(sim,podPlug.RUN_NAME)

# go go go  ..........
sim.run()