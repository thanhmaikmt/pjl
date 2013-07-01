from MBmusic import *
from MBmidi import *
from MBsetup import *
from MBoscserver import *
import players


_context=None


class MBError:
    
    def __init__(self, msg):
        self.msg = msg
            
    def get_message(self):
        return self.msg   
    
    def __str__(self):
        return self.get_message()                 
   
class Context:
        
    def __init__(self,seqtype=Sequencer):
        self.mid = MidiEngine()
        self.midi_out_dev = self.mid.open_midi_out(MIDI_OUT_NAMES)
        self.seq = seqtype()
        self.players=16*[None]
        
    def allocate_player(self,chan):
        inst=self.midi_out_dev.allocate_channel(chan)
        assert self.players[chan] == None
        self.players[chan]=players.BasicPlayer(inst,None,None)
        return self.players[chan]
        
        
    def start(self,map):
        addr=MB.get_osc_ip()
        self.osc_driver=Server(addr,map,None)
        self.osc_driver.run()
        self.seq.start()
        
    def get_sequencer(self):
        return self.seq
        
    def quit(self):
        
        self.seq.quit()
        print ' Stopping midi engine '  
        self.mid.quit()
        self.osc_driver.quit()

def init():
    """
    Initialize the system by creating a context.
    This will start the midi system.
    """
    global _context
    
    if _context:
        raise MBError(" Already inited ")

    _context=Context()
    
    return _context
    
def create_player(chan):
    """
    Create a Player
    """ 
    p=_context.allocate_player(chan)
    return p
 

def start(map):
    """
    Start the context. Sequencer will start running
    map is a dictionary of OSC keywords to a routine that processes it
    e.g.
    def melody_func(toks,data):
         . . .
         
    map={melody:melody_fuc}
    """
    
    _context.start(map)
    
 
def quit():
    _context.quit()
     
def deprecated():   
    assert False
    
class Band:
    """
    Wrapper for instruments/players/sequencer
    """
    def __init__(self,seqtype=Sequencer):
        
        
        deprecated()    
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


