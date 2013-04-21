
import music
from pjlmidi import *
from mbconstants import  *
import osc_driver
import math

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
    
    #metro = music.Metro(0, 4,seq, metro_inst, accent, weak) 
    
    # bass line

    
    class BassData:
        
        def __init__(self):
            self.times =   [0.0,  1.0, 2.0, 3.0]
            self.vels =    [100,  70,  90,  70]                 
            self.durs =    [0.6, 0.4, 0.4 , 0.4]
            self.pattern=  [0,   2,  4,  2]


    bass_inst = midi_out_dev.allocate_channel(1)  
    bass_player = music.BassPlayer(seq, bass_inst, score,30,48)
    bass_data=BassData()
    bass_factory=music.GrooverFactory(seq,bass_data,bass_player)
    music.Repeater(0, 4, seq, bass_factory) 
    
    # Vamp
       
    vamp_inst = midi_out_dev.allocate_channel(0)
    vamp = music.ChordPlayer(seq, vamp_inst, score, 50,[0,1,2,3])

    class VampData:
        
        def __init__(self):
            self.times = [0.5, 1.5, 2.0]
            self.vels =  [80,  70,  70]                 
            self.durs =  [0.6, 0.4, 0.4]
       
            
   
    vamp_data=VampData()
    factory=music.GrooverFactory(seq,vamp_data,vamp)   
    music.Repeater(0, 4, seq, factory) 
    
    solo_inst=midi_out_dev.allocate_channel(2)
    
    # ready to go
    
    seq.start()
    
    class Wrapper:
        
        def set_push1(self,i,val):
            print "set tonality",i,val
            if val > 0:
                score.set_tonality(music.tonalities[(i-1)%7])

        def set_xy(self,x,y):
            print "set xy",x,y
            
        def set_accel(self,x,y,z):
            print "accel ",x,y,z
            
            
        def set_push2(self,i,val):
            vel=int(val*100)       
            pitch=score.get_tonality().get_note_of_scale(i,score.key)+36
            #print "play",i,vel
            if vel != 0:
                solo_inst.note_on(pitch,vel)
            else:
                solo_inst.note_off(pitch)
            
    wrapper=Wrapper()
    
    osc_driver.run(wrapper)
    
    seq.quit()
 
    mid.quit()
    
    
except MidiError as e:
    
    print e.get_message()

 
