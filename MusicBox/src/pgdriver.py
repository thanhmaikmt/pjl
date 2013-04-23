import pygame, sys,os
import threading
from pygame.locals import * 


class PGDriver(threading.Thread):
    
    def __init__(self,client):      
        threading.Thread.__init__(self)   
        pygame.init() 
         
        window = pygame.display.set_mode((468, 60)) 
        pygame.display.set_caption('Music Box') 
        self.running=False
        self.client=client
        
        
    def process(self,events):
        
        for event in events: 
            if event.type == QUIT:
                self.running=False 
            else: 
                self.client.handle(event) 

        
    def run(self):
        
        print "PGDRIVER RUN"
        self.running=True
        while self.running:
            self.process(pygame.event.get())
            
            
            
    def stop(self):  
        
        print "pgdriver Waiting for Server-thread to finish"
        self.running=False
        self.join() ##!!!
        print "pgdriver joined Done"
        pygame.quit()     #   TODO check that midi subsystem is notconfused by this
        
    
if __name__ == "__main__":
    
    pe=PGDriver(None) 
    pe.start()
    
    xxx=raw_input("CRto QUIT:")
    
    pe.stop()
       
                      