    
from pjlmidi import  *  
from mbconstants import *    
 
#  create PyMidi to initialize misi system.



mid=MidiEngine()

midi_out=mid.open_midi_out(MIDI_OUT_NAMES)
midi_in=mid.open_midi_in(MIDI_IN_NAMES)   
            
     
        
# define input and output channels
# adjust these for hardware reported by above

print midi_in,midi_out


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
#        for e in evts:
#            e[0][0]+=1
           
    midi_out.out.write(evts)
    print (evts)
 
# register the handler
mid.set_callback(myhandler) 
   
# start deamon
mid.start()



tt=raw_input("Hit cr to quit:")
#wait a few secs then halt
mid.halt()

