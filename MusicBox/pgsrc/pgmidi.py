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
        
    def __init__(self,midi_in=1,midi_out=0):
        pygame.init()
    
    
        pygame.fastevent.init()
        event_get = pygame.fastevent.get
        event_post = pygame.fastevent.post
        
        pygame.midi.init()
    
    
        _print_device_info()
        
        self.midi_in = pygame.midi.Input(midi_i)
    #window = pygame.display.set_mode((468, 60))
    
    
        instruments=[6,28,13]
    
        self.midi_out = pygame.midi.Output(midi_o, 0)
    
        for i in range(len(instruments)):
            self.midi_out.set_instrument(instruments[i],i)

        threading.Thread.__init__(self);

    def run(self):         
        self.running=True
        while self.running:       
            if self.midi_in.poll():
                midi_events = self.midi_in.read(10)
            
                for x in midi_events:
                        print (x)
            
                self.midi_out.write(midi_events)
                time.sleep(0.0001) 
            
    def stop(self):
        self.runningg=False
        del self.midi_in
        del self.midi_out
        
        pygame.midi.quit()
        
        #
if __name__ == "__main__":
    
    midi_i = 3 ; midi_o = 8;
    
    e=PgMidi()
    e.start()
    
    