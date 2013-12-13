import sys
sys.path.append('beat')

from MBmusic import *
import beatclient

from MBmidi import *
from MBsetup import *
from MBoscserver import *
from players import *
import MBsetup


_context=None


class MBError:
    
    def __init__(self, msg):
        self.msg = msg
            
    def get_message(self):
        return self.msg   
    
    def __str__(self):
        return self.get_message()                 
   
class Context:
        
    def __init__(self,seqtype=Sequencer,beat_analysis=False):
        global _context
        assert _context == None
        self.mid = MidiEngine()
                              
        try:                      
            self.midi_out_dev = self.mid.open_midi_out(MIDI_OUT_NAMES)
        except MidiError:
            MBsetup.start_midi_synth()
            time.sleep(8)
            self.midi_out_dev = self.mid.open_midi_out(MIDI_OUT_NAMES)
            
            
        self.seq = seqtype()
        self.players=16*[None]
        if beat_analysis:
            self.beat_client=beatclient.Client(debug=False)
        else:
            self.beat_client=None
            
        self.default_parser=BasicParser()
        _context=self
        
        self.bar_length=None
        
        self.frozen=False       # keep sampling bar/beats until true
        
    def create_player(self,chan,pipe_to_beat):
        inst=self.midi_out_dev.allocate_channel(chan)
        assert self.players[chan] == None
        if pipe_to_beat:
            bc=self.beat_client
        else:
            bc=None
            
        self.players[chan]=Player(inst,self,parser=self.default_parser,seq=self.seq,memory=True,beat_client=bc)
        return self.players[chan]
        
        
    def start(self,map):
        """
        Start the context. Sequencer will start running
        
        if map is not None a OSC server is started to recieve messages.
        
        map is a dictionary of OSC keywords to a routine that processes it
        e.g.
        def melody_func(toks,data):
             . . .
             
        map={melody:melody_fuc}
        """
        
        if map:
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
        
    
    def freeze(self):
        if self.frozen:
            print "Already frozen"
            return
        
        self.frozen=True
        
        print " Freezing: ",self.beat_length, self.bar_length
        
    def get_barlength(self):
        if not self.frozen:
            self.bar_length=self.beat_client.get_barlength()
            
        return self.bar_length 
    
    def get_beatlength(self):
       
        if not self.frozen:
            self.beat_length=self.beat_client.get_beatlength()
       
        return self.beat_length

    
   