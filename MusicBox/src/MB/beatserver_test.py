## --- test code 


import beatserver
import time

tt=0.0
beatserver.graph=True
scat=0.003
probs=[.9,.2,.6,.6]

cnt=0
import random
for _ in range(100):
    time.sleep(1)
    if probs[cnt]> random.random():
        beatserver.stomper.add_event(tt*(1+random.random()*scat),1.0)
        
    beatserver.analysis.doit()
    tt+=0.5
    cnt = (cnt+1)%4
        