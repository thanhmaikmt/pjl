
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
     
        
    seq=Sequencer()
    seq.schedule_phrase(0,phrase,Player())
    
    seq.start()
    


        
    