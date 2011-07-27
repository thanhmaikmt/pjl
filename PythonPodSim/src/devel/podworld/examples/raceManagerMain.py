#
#
import world 
import simulation
import sys
import os
import imp


# See 
#http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder


pods=[]

names=["fred","pjl"]

for name in names:
    punters_path="../punters/"+name
    sys.path.append(punters_path)
    fin=open(punters_path+"/"+name+"_plugin.py",'r')
    punter_mod=imp.load_source(name,punters_path+"/",fin)
    sys.path.remove(punters_path)   
    default_dir=os.getcwd()
    pod   = pods.CarPod()
    os.chdir(punters_path)
    
    # call the pluginto equip the car 
    punter_mod.equip_car(pod)
    pods.append(pod)
    os.chdir(default_dir)


###  START OF PROGRAM

dt    = .1
world = world.World("rect_world.txt",dt,pods)
sim   = simulation.Simulation(world,"Example")
sim.run()