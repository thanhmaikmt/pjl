import pygame.midi as midi
import threading
import time
import atexit




class Device:
    
    def __init__(self,id,interf, name, input, output, opened):
        self.id=id
        self.interf=interf
        self.name=name
        self.input=input
        self.output=output
        self.opened=opened
        
    
class Engine(threading.Thread):
        
    def __init__(self):
        midi.init()
                # register tidy up function to be called at exit.
    
        threading.Thread.__init__(self);
        #atexit.register(self.halt)
        # defualt handler prints midi evts
        self.handler=self.default_handler
        self.midi_in = None
        self.midi_out = None
        
    def device_info(self):
        devs=[]
        for i in range( midi.get_count()):
            r = midi.get_device_info(i)
            (interf, name, input, output, opened) = r
            devs.append(Device(i,interf, name, input, output, opened))
            in_out = ""
            if input:
                in_out = "(input)"
            if output:
                in_out = "(output)"
    
            print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
                   (i, interf, name, opened, in_out))
            
        return devs
            
    def set_midi_in(self,midi_in):    
        self.midi_in = midi.Input(midi_in)
    
    
    def set_midi_out(self,midi_out):    
        self.midi_out = midi.Output(midi_out, 0)
    

    def default_handler(self,evts):
        print (evts)

    def write(self,evts):
        self.midi_out.write(evts)
                
    def set_callback(self,handler):
        self.handler=handler
        
    def run(self):         
        self.running=True
        
        while self.running:       
            if self.midi_in.poll():
                midi_events = self.midi_in.read(10)
                self.handler(midi_events)
            else:
                time.sleep(0.001)
                 
        print " quitting pgmidi deamon"
            
    def halt(self):
        
        print  "Halting"
        if not self.running:     # make sure we don't do this twice
            return
        
        self.running=False      # flag deamon to halt.
        self.join()             # wait for thread to halt
        print  "Halting 2"
        self.cleanup()
        
    def cleanup(self):
        # send all note off event to avoid hanging.
        
        evts=[[[0b10110000,120,0],0]]
        self.midi_out.write(evts)
     
        # clean up
        if self.midi_in != None:
            del self.midi_in
        if self.midi_out != None:
            del self.midi_out
     
        print  "Halting 3"
     
        midi.quit()
           
        print  "Halting 4"
     
     
 