import  pygame
import  sys,os
#from pygame.locals import * 


class PGDriver:
    
    """
    pygame frontend for events.
    delegates the interpretation of events to a user supplied cleint.
    """
    
    def __init__(self,client,dim=(256, 256)):      
       # threading.Thread.__init__(self)   
        pygame.init() 
         
        window = pygame.display.set_mode(dim) 
        pygame.display.set_caption('Music Box') 
        self.running=False
        self.client=client
        
        
    def process(self,event):
        
            if event.type == pygame.QUIT or  (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                print "QUITING"
                self.running=False 
                
            else: 
                self.client.handle(event) 

        
    def run(self):
        
        print "PGDRIVER RUN"
        self.running=True
        while self.running:
            self.process(pygame.event.wait())
        print "PGDRIVER QUIT"
        
            
            
    def stop(self):  
        pygame.event.clear()      
        pygame.quit()     #   TODO check that midi subsystem is notconfused by this
        print " STOPPED"
    
if __name__ == "__main__":
    
    class Client:
        
        def handle(self,event):
            print event
            
            
            
            
    pe=PGDriver(Client()) 
    pe.run()
    print "EXITING"
    sys.exit(-1)
    print " EXITTED"
#    pe.stop()
       
                      