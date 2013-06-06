from MBmusic import *
from MBmidi import *
from MBsetup import *
from MBoscserver import *


class Band:
    """
    Wrapper for instruments/players/sequencer
    """
    def __init__(self,seqtype=Sequencer):
        
        mid = MidiEngine()
        
        midi_out_dev = mid.open_midi_out(MIDI_OUT_NAMES)
            
        seq = seqtype()
        # MetroNome
        accent = NoteOn(61, 100)
        weak = NoteOn(60, 80)
        metro_inst = midi_out_dev.allocate_channel(9)
        
        self.metro = Metro(0, 4,seq, metro_inst, accent, weak) 
    
        self.bass_inst = midi_out_dev.allocate_channel(1)  
        # Vamp
        self.vamp_inst = midi_out_dev.allocate_channel(0)
        self.solo_inst = midi_out_dev.allocate_channel(2)
        self.solo_mesenger=Messenger(self.solo_inst)
 
        self.seq=seq
        self.mid=mid
        
    def start(self):
        self.seq.start()
        
    def quit(self):
        
        self.seq.quit()
        print ' Stopping midi engine '  
        self.mid.quit()


