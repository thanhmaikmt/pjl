import pygame
import pygame.locals as pgl
import pygame.midi 
from   pygame.locals import *
import threading
import time

try:  # Ensure set available for output example
    set
except NameError:
    from sets import Set as set



def _print_device_info():
        for i in range( pygame.midi.get_count() ):
            r = pygame.midi.get_device_info(i)
            (interf, name, input, output, opened) = r
    
            in_out = ""
            if input:
                in_out = "(input)"
            if output:
                in_out = "(output)"
    
            print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
                   (i, interf, name, opened, in_out))
 
class PgMidi(threading.Thread):
        
    def __init__(self):
        pygame.init()
    
    
        #pygame.fastevent.init()
        #event_get = pygame.fastevent.get
        #event_post = pygame.fastevent.post
        
        pygame.midi.init()
    
        _print_device_info()
        threading.Thread.__init__(self);
    
    def set_midi_in(self,midi_in):    
        self.midi_in = pygame.midi.Input(midi_in)
    #window = pygame.display.set_mode((468, 60))
    
    def set_midi_out(self,midi_out):    

        instruments=[6,28,13]
    
        self.midi_out = pygame.midi.Output(midi_out, 0)
    
        for i in range(len(instruments)):
            self.midi_out.set_instrument(instruments[i],i) 



    def run(self):         
        self.running=True
        
        while self.running:       
            if self.midi_in.poll():
                midi_events = self.midi_in.read(10)
                
                print (midi_events)
                
                if not self.running:
                    break
                self.midi_out.write(midi_events)
                if not self.running:
                    break
               
            else:
                time.sleep(0.001)
                 
        print " quitting pgmidi deamon"
            
    def halt(self):
        self.running=False 
   
        print " Halt 1"
        self.join()
        print " halt 2"
         
    #window = pygame.display.set_mode((468, 60))
    
        evts=[[[0b10110000,120,0],0]]

        self.midi_out.write(evts)
        print " halt 3"
     
        del self.midi_in
        del self.midi_out
        
        print " halt 4"
     
        pygame.midi.quit()
        print " halt 5"
     
        pygame.quit()
        print " Halt 6"
        
        
        
        #
if __name__ == "__main__":
    
    e=PgMidi()
    e.set_midi_in(3)
    e.set_midi_out(5)
    e.start()
    time.sleep(4)
    e.halt()
    
    