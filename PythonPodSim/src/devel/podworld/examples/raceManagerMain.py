#
#   Showing how to 
# 
# 
from world import  *
from agent import *
from painter import *
from pool import  *
from admin import  *
from simulation import *
import sys
import os
import imp



#http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder



pods=[]

names=["fred","pjl"]

for name in names:
    my_path="punters/"+name
    sys.path.append(my_path)
    fin=open("punters/"+name+"/"+name+"_plugin.py")
    py_mod=imp.load_source(name,"punters/"+name+"/",fin)
    sys.path.remove(my_path)   
    defaultDir=os.getcwd()
    #    
    pod   = CarPod()
    os.chdir("punters/"+name)
    
    # call the pluginto equip the car 
    py_mod.equip_car(pod)
    pods.append(pod)
    os.chdir(defaultDir)


###  START OF PROGRAM

dt    = .1
world = World("rect_world.txt",dt,pods)
sim   = Simulation(world,"Example")
sim.run()