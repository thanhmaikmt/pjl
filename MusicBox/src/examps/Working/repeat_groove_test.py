
import MB

  
if __name__ == "__main__":    
    
        
    seq=MB.Sequencer()
        
    
    class P:
        
        def play_count(self,count):
            print count
        
       
         
         
    p=P()
    
    class Factory:
        def create(self,when):
            print " Factory create"
            
    factory=Factory()
    
    mess=MB.Repeater(0,4,seq,factory)
    
    seq.start()
    


        
    