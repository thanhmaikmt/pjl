
import music
from pjlmidi import *
import mbconstants as mb
import oscdriver
import math
import sys
import traceback
import players

try:
    mid = MidiEngine()
    
    midi_out_dev = mid.open_midi_out(MIDI_OUT_NAMES)
        
    seq = music.Sequencer(ticks_per_beat=2 * 2 * 3 * 5, bpm=100)
    
    # Score
    beats_per_bar=4
    bars_per_section=1
    key=music.G
    start=0
    
    score = music.Score(start, seq, bars_per_section,beats_per_bar,key)
    score.set_tonality(music.I, 0)
    

    # MetroNome
    accent = music.NoteOn(61, 100)
    weak = music.NoteOn(60, 80)
    metro_inst = midi_out_dev.allocate_channel(9)
    
    metro = music.Metro(0, 4,seq, metro_inst, accent, weak) 
    
    # bass line

    
    class BassData:
        
        def __init__(self):
            self.times =   [0.0,  1., 2.0, 3.0]
            self.vels =    [100,  70,  90,  70]                 
            self.durs =    [0.6, 0.4, 0.4 , 0.4]
            self.pattern=  [0,   0,  0,  0]


    bass_inst = midi_out_dev.allocate_channel(1)  
    bass_player = music.BassPlayer(seq, bass_inst, score,30,48)
    bass_data=BassData()
    bass_factory=music.GrooverFactory(seq,bass_data,bass_player)
    music.Repeater(0, 4, seq, bass_factory) 
    
    # Vamp
    vamp_inst = midi_out_dev.allocate_channel(0)
  
    
    vamp = music.ChordPlayer(seq, vamp_inst, score, 60,[0,1,2])
    
    if False:
        class VampData:
            
            def __init__(self):
                self.times = [0.5, 1.5, 2.0]
                self.vels =  [80,  70,  70]                 
                self.durs =  [0.6, 0.4, 0.4]
           
                
        vamp_data=VampData()
        factory=music.GrooverFactory(seq,vamp_data,vamp)   
        music.Repeater(0, 4, seq, factory) 
    
    solo_inst=midi_out_dev.allocate_channel(2)
    solo_player=music.Player(solo_inst)
    # ready to go
    
    seq.start()
    
    
   
       
    class Client:
        
        def __init__(self):
            self.map={"melody":self.melody,
                      "tonality":self.tonality,
                      "chordNote":self.chordNote,
                      "chord":self.chord}
            self.chord_player=players.ChordPlayer(vamp_inst,score)
            self.melody_player=players.MelodyPlayer(solo_player,score,seq)
            
        def handle(self,addr,data):
            
            print addr,data
#            self.session.record(addr,data)
            
            toks=addr.split('/')
            
            if len(toks) < 3:
                return
            
            func=self.map.get(toks[2])
            
            if func != None:
                func(toks[3:],data)
            else:
                print " No musicbox handler for:", addr
            
        def tonality(self,toks,data):
            
            val1=int(toks[0])
            val2=int(toks[1])
            trig=float(data[0])
            print "set tonality",val1,val2
            if val2 > 0:
                score.set_tonality(music.tonalities[((val1-1)*5+(val2-1))%7])
         
            print toks
            
            
        def chord(self,toks,data):
            
            self.chord_player.play(toks,data)
            
                            
            

        def chordNote(self,toks,data):
            
            print "chordNote",toks,data
           
        def melody(self,toks,data):
            """
            Plays a note of the scale in the current tonality
            """
            
            self.melody_player.play(toks,data)
            
            
                    
    client=Client()
    
    
    drivers=[]
    
    
    addr=mb.get_osc_ip()
    osc_driver=oscdriver.OSCDriver(client,addr)
    osc_driver.run()
    drivers.append(osc_driver)
    
            
    xxx=raw_input(" HIT CR ")
      
    
except:
    
    #print e.get_message()
    traceback.print_exc()
    

finally:
    
    print 'Stopping drivers: '  
    
    for drv in drivers:
        print drv
        drv.stop()
        
        
        
    seq.quit()
    print ' Stopping midi engine '  
    mid.quit()
    
    print 'Thats it ! '  
    
    sys.exit(0)
 
