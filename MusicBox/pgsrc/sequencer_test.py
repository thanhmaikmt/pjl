import threading
import engine
import linkedlist
from music import *
import sys


            
     
        
if __name__ == "__main__":
    # test code
    #  create PyMidi to initialize misi system.
    import pymidi
    mid=pymidi.PyMidi()

    
    # print devicess
    mid.print_device_info()
    
    # define input and output channels
    # adjust these for hardware reported by above
    mid.set_midi_out(1)
    
    #
    #  simplest possible sequence
    class Sequence:
                  
        def play_events_at(self,tick):
            
            note=60+(tick/2)%12
            
            if tick % 2 == 0 :
                mid.midi_out.note_on(note, velocity=100, channel = 1)
            else:
                mid.midi_out.note_off(note, velocity=0, channel = 1)
            #print tick


    seq=Sequence()
    
    sequencer=Sequencer()
    
    sequencer.add_sequence(seq)
    
    sequencer.start()
    
    tt=raw_input("Hit cr to quit:")
    #wait a few secs then halt
    
    mid.cleanup()