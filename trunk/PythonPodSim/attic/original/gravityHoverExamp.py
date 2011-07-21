from simulation import *
#
#     get the gravity pod to hover at y=yHover
#

yHover   =  300
dydtMin  = -100
dydtMax  =  10

class HoverControl:

    def process(self,sensor,state,dt):

        control=Control()

        if state.y > yHover:
           if state.dydt > dydtMin:
              control.up=1

        if state.dydt > dydtMax:
            control.up=1

        return control


dt          =.1
brain       = HoverControl()
nSensors    = 40
sensorRange = 2000
pod         = GravityPod(nSensors,sensorRange,brain,(255,0,0))
pods        = [pod]
world       = World("rect_world.txt",pods)
sim         = Simulation(world,dt)
#uncomment the next line to hide the walls.
#sim.world.blind=True

sim.run()
