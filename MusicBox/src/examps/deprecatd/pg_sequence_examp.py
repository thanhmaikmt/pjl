import MBmidi
import time
from music import  *



def call_back(tick):
    print tick
    
    if tick%ticks_per_beat == 0:
        midi.write()
    
 
def idle():
    pass
       
    
ticks_per_beat=3*4*5
bpm=60

seq=Engine(bpm,ticks_per_beat,call_back,idle)


midi=pymidi.PyMidi()
    
midi.print_device_info()
    
    # adjust these for hardware reported by above
midi.set_midi_in(3)
midi.set_midi_out(5)
    
# simple handler to pass events to midi_out device
def myhandler(evts):
        midi.midi_out.Write(evts)
        
midi.set_callback(myhandler) 
       
    # start deamon
    
seq.start()
midi.start()
    
    #wait a few secs then halt
    
    
time.sleep(30)

midi.halt()

seq.halt()

