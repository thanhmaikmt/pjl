import pygame.midi as midi
import threading
import time
import atexit


class PyMidi(threading.Thread):
        
    def __init__(self):
        midi.init()
                # register tidy up function to be called at exit.
    
        threading.Thread.__init__(self);
        
        # defualt handler prints midi evts
        self.handler=self.default_handler
        
    def print_device_info(self):
        for i in range( midi.get_count()):
            r = midi.get_device_info(i)
            (interf, name, input, output, opened) = r
    
            in_out = ""
            if input:
                in_out = "(input)"
            if output:
                in_out = "(output)"
    
            print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
                   (i, interf, name, opened, in_out))
            
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
     
        # send all note off event to avoid hanging.
        
        evts=[[[0b10110000,120,0],0]]
        self.midi_out.write(evts)
     
        # clean up
        del self.midi_in
        del self.midi_out
     
        print  "Halting 3"
     
        midi.quit()
           
        print  "Halting 4"
     
     
        
if __name__ == "__main__":
    
    # test code
    #  create PyMidi to initialize misi system.
    mid=PyMidi()

    
    # print devicess
    mid.print_device_info()
    
    # define input and output channels
    # adjust these for hardware reported by above
    mid.set_midi_in(3)
    mid.set_midi_out(5)
    
    
    #evts=[[[0b10110000,0,120],0],[[0b10110000,32,0],0]]
    #mid.midi_out.write(evts)
    #vts=[[[0b10110000,0,120],0],[[0b10110000,32,0],0]]
    #mid.midi_out.write([[[0xc0,0],0]])
    
        
    # simple handler to pass events to midi_out device
    # define a hander for midi events
    def myhandler(evts):
        """
        This version prints then forwards event to the midi out.
        """
        for e in evts:
            e[0][0]+=9
               
        mid.midi_out.write(evts)
        print (evts)
     
    # register the handler
    mid.set_callback(myhandler) 
       
    # start deamon
    mid.start()
    
    
    
    tt=raw_input("Hit cr to quit:")
    #wait a few secs then halt
    mid.halt()
    
    