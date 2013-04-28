
import music 
import MBmidi 
import MB

  
if __name__ == "__main__":    
    
    mid=MBmidi.MidiEngine()

    midi_out=mid.open_midi_out(MB.MIDI_OUT_NAMES)
    
    inst=MBmidi.Instrument(midi_out.out,1)
    

    phrase=music.Phrase()
    phrase.add(0,music.NoteOn(60,90))
    phrase.add(1,music.NoteOff(60))
    phrase.add(3,music.NoteOn(61,90))
    phrase.add(4,music.NoteOff(61))    
    phrase.add(3,music.NoteOn(66,90))
    phrase.add(4,music.NoteOff(66))
    phrase.add(2,music.NoteOn(60,90))
    phrase.add(5,music.NoteOff(60))
   
    

    seq=music.Sequencer(beats_per_sec=2.0)
    seq.schedule_phease(0,phrase,music.Player(inst))
    
    seq.start()
    


        
    