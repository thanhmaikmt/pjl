
from music import *

  
if __name__ == "__main__":    
    
 
    
        
    seq=Sequencer()
    
        
        
    class Mess(Event):
        
        def __init__(self,tick,data):
            self.tick=tick
            
            Event.__init__(self, tick, data,None)
            
        
        def send(self):
            print " Send "  
            self.tick+=3
            seq.add(self)
             #TODO delete etc.....
            
         
         
    mess=Mess(0,None)
    seq.add(mess)
    
    seq.start()
    


        
    