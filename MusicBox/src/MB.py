import MBmusic
import beatclient

from MBmidi import *
from MBsetup import *
from MBoscserver import *
from players import *


_context=None


class MBError:
    
    def __init__(self, msg):
        self.msg = msg
            
    def get_message(self):
        return self.msg   
    
    def __str__(self):
        return self.get_message()                 
   
class Context:
        
    def __init__(self,seqtype=MBmusic.Sequencer,beat_analysis=True):
        global _context
        assert _context == None
        self.mid = MidiEngine()
        self.midi_out_dev = self.mid.open_midi_out(MIDI_OUT_NAMES)
        self.seq = seqtype()
        self.players=16*[None]
        if beat_analysis:
            self.beat_client=beatclient.Client(debug=False)
        else:
            self.beat_client=None
            
        self.default_parser=BasicParser()
        _context=self
        
    def allocate_player(self,chan):
        inst=self.midi_out_dev.allocate_channel(chan)
        assert self.players[chan] == None
        self.players[chan]=Player(inst,parser=self.default_parser,seq=self.seq,memory=True,beat_client=self.beat_client)
        return self.players[chan]
        
        
    def start(self,map):
        """
        Start the context. Sequencer will start running
        map is a dictionary of OSC keywords to a routine that processes it
        e.g.
        def melody_func(toks,data):
             . . .
             
        map={melody:melody_fuc}
        """
  
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
        self.beat_client.quit()
        
    def callback(self,func,start,period):
        """
        func --- Call back called on same thread as midi so don't do too much here
        """
        MBmusic.Repeater(start,period,self.seq,func)
        
    
    def get_barlength(self):
        return self.beat_client.get_barlength()
    
    def get_beatlength(self):
        return self.beat_client.get_beatlength()

    
    def create_player(self,chan):
        """
        Create a Player
        """ 
        p=_context.allocate_player(chan)
        return p
     
    
  
def deprecated():   
    assert False
    
class Band:
    """
    Wrapper for instruments/players/sequencer
    """
    def __init__(self,seqtype=MBmusic.Sequencer):
        
        
        deprecated()    
        mid = MidiEngine()
        
        midi_out_dev = mid.open_midi_out(MIDI_OUT_NAMES)
            
        seq = seqtype()
        # MetroNome
        accent = MBmusic.NoteOn(61, 100)
        weak = MBmusic.NoteOn(60, 80)
        metro_inst = midi_out_dev.allocate_channel(9)
        
        self.metro = MBmusic.Metro(0, 4,seq, metro_inst, accent, weak) 
    
        self.bass_inst = midi_out_dev.allocate_channel(1)  
        # Vamp
        self.vamp_inst = midi_out_dev.allocate_channel(0)
        self.solo_inst = midi_out_dev.allocate_channel(2)
        self.solo_mesenger=MBmusic.Messenger(self.solo_inst)
 
        self.seq=seq
        self.mid=mid
        
    def start(self):
        self.seq.start()
        
    def quit(self):
        
        self.seq.quit()
        print ' Stopping midi engine '  
        self.mid.quit()


