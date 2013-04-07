
from music import *
from pjlmidi import *
from setup import *

  
if __name__ == "__main__":    
    
    mid=MidiEngine()

    midi_out=mid.open_midi_out(MIDI_OUT_NAME)
    
    inst=Instrument(midi_out,1)
    

    phrase=Phrase()
    phrase.add(0,NoteOn(60,90))
    phrase.add(1,NoteOff(60))
    phrase.add(3,NoteOn(61,90))
    phrase.add(4,NoteOff(61))    
    phrase.add(3,NoteOn(66,90))
    phrase.add(4,NoteOff(66))
    phrase.add(2,NoteOn(60,90))
    phrase.add(5,NoteOff(60))
   
    
   
         
    ticks_per_beat=2*2*3*5
    seq=Sequencer(ticks_per_beat=ticks_per_beat,bpm=120)
    seq.schedule_at(0,phrase,Player(inst))
    
    seq.start()
    


        
    