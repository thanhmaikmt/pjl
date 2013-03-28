
from music import *

  
if __name__ == "__main__":    
    
        
    seq=Sequencer(ticks_per_beat=1,bpm=120)
        
    class Repeater(Event):
        
        def __init__(self,time):
            self.time=time
            
            Event.__init__(self, time)
            
        
        def fire(self):
            print " Send "  
            self.time+=3
            seq.add(self)
             #TODO delete etc.....
            
         
         
    mess=Repeater(0)
    seq.add(mess)
    
    seq.start()
    


        
    