import pg_engine as engine
import time




def call_back(tick):
    print tick
    
 
def idle():
    pass
       
    
    
ticks_per_beat=3*4*5
bpm=60

e=engine.Engine(bpm,ticks_per_beat,call_back,idle)


e.start()

