import pygame, sys,os
import threading
from pygame.locals import * 


class PGDriver:
    
    def __init__(self,client):      
       # threading.Thread.__init__(self)   
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
        
        pygame.quit()     #   TODO check that midi subsystem is notconfused by this
        
    
if __name__ == "__main__":
    
    class Client:
        
        def handle(self,event):
            print event
            
            
            
            
    pe=PGDriver(Client()) 
    pe.run()
    
    pe.stop()
       
                      