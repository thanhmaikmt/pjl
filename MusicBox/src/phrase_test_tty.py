
from music import *

  
if __name__ == "__main__":    
    
    phrase=Phrase()
    phrase.add(0,"one")
    phrase.add(3,"three")
    phrase.add(4,"four")
    phrase.add(2,"two")
    phrase.add(2,"anothertwo")
   
   
        
                     
    
    class Player:
        
        def play(self,event):
            print event
    
    
    worker1=Scheduler(phrase,Player())
   
    
        
    seq=Sequencer()
    worker1.schedule(0,10,seq)
    
    seq.start()
    


        
    