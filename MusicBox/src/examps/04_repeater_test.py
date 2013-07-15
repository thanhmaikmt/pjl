import sys
sys.path.append('../MB')

import MBmusic

  
if __name__ == "__main__":    
    
        
    seq=MBmusic.Sequencer()
        
    
    
    class Factory:
        def create(self,when):
            print " Factory create",when
            
    factory=Factory()
    
    mess=MBmusic.Repeater(3,2.5,seq,factory.create)
    
    seq.start()
    


        
    