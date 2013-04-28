    
import MBmidi   
import MB   
import time
#  create PyMidi to initialize misi system.



mid=MBmidi.MidiEngine()

midi_out=mid.open_midi_out(MB.MIDI_OUT_NAMES)
  
            
inst=MBmidi.Instrument(midi_out.out,0)     

        



for pitch in range(48,60):
    print pitch
    inst.note_on(pitch, 120)
    time.sleep(.3)
    inst.note_off(pitch)
    
    
#wait a few secs then halt
mid.quit()

