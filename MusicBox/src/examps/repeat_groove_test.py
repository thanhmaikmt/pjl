
from music import *

  
if __name__ == "__main__":    
    
        
    seq=Sequencer()
        
    
    class P:
        
        
        def play_count(self,count):
            print count
        
       
         
         
    p=P()
    mess=Repeater(0,4,seq,Groove,deltas=[0.5,1.0,.5],player=p)
    
    seq.start()
    


        
    