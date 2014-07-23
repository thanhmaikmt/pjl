import sys
sys.path.append('../MB')

import MBmusic


    
seq=MBmusic.SequencerBPM()
    

class Player:
    
    def play_count(self,count,data,beat):
        print count,seq.beat,data.times[count]+when,beat
 
class Data:
    
    def __init__(self):
        self.times =   [0.3,  1.0, 2.0, 3.0]
     
player=Player()
when=1.2
data=Data()
groover=MBmusic.Groover(when,seq,data,player)




seq.start()
    


        
    