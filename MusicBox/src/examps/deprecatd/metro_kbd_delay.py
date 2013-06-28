
import MBmusic
import MBmidi
import MBsetup
import math
import traceback

try:
    mid = MBmidi.MidiEngine()
    
    midi_out_dev = mid.open_midi_out(MBsetup.MIDI_OUT_NAMES)
    
    
    seq = MBmusic.SequencerBPM(beats_per_sec=1.0)
    
    # Score
    beats_per_bar=4
    bars_per_section=1
    key=MBmusic.G
    start=0
    
    

    # MetroNome
    accent = MBmusic.NoteOn(61, 100)
    weak = MBmusic.NoteOn(60, 80)
    metro_inst = midi_out_dev.allocate_channel(9)
    metro = MBmusic.Metro(0, 4,seq, metro_inst, accent, weak) 
    
        
    solo_inst=midi_out_dev.allocate_channel(2)
    solo_player=MBmusic.Player(solo_inst)
    
    
    # ready to go
    
    seq.start()
    
        
    
    
    
except:
    
    traceback.print_exc()

finally:
    seq.quit()
    mid.quit()