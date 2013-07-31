import sys
sys.path.append('../MB')

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
    
    score = MBmusic.Score( bars_per_section,beats_per_bar,key)
    score.set_tonality(MBmusic.I, 0)
    

    # MetroNome
    accent = MBmusic.NoteOn(61, 100)
    weak = MBmusic.NoteOn(60, 80)
    metro_inst = midi_out_dev.allocate_channel(9)
    
    #metro = MBmusic.Metro(0, 4,seq, metro_inst, accent, weak) 
    
    # bass line

    
    class BassData:
        
        def __init__(self):
            self.times =   [0.0,  1.0, 2.0, 3.0]
            self.vels =    [100,  70,  90,  70]                 
            self.durs =    [0.6, 0.4, 0.4 , 0.4]
            self.pattern=  [0,   2,  4,  2]


    bass_inst = midi_out_dev.allocate_channel(1)  
    bass_player = MBmusic.BassPlayer(seq, bass_inst, score,30,48)
    bass_data=BassData()
    bass_factory=MBmusic.GrooverFactory(seq,bass_data,bass_player)
    MBmusic.Repeater(0, 4, seq, bass_factory.create) 
    
    # Vamp
       
    vamp_inst = midi_out_dev.allocate_channel(0)
    vamp = MBmusic.ChordPlayer(seq, vamp_inst, score, 60,[0,1,2,3])

    class VampData:
        
        def __init__(self):
            self.times = [0.5, 1.5, 2.0]
            self.vels =  [80,  70,  70]                 
            self.durs =  [0.6, 0.4, 0.4]
       
            
   
    vamp_data=VampData()
    factory=MBmusic.GrooverFactory(seq,vamp_data,vamp)   
    MBmusic.Repeater(0, 4, seq, factory.create) 
    
    solo_inst=midi_out_dev.allocate_channel(2)
    solo_player=MBmusic.Messenger(solo_inst)
    # ready to go
    
    seq.start()
    
    class Wrapper:
        
        def set_push1(self,i,val):
            print "set tonality",i,val
            if val > 0:
                score.set_tonality(MBmusic.tonalities[((i-1)*5)%7])

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
                # schedule the note off
                playable = MBmusic.Playable(MBmusic.NoteOff(pitch), solo_player)
                seq.add_after(.1, playable)
            
    wrapper=Wrapper()
    
    while True:
        xx=raw_input("Enter root: [0-6]")
        ii=int(xx)
        if ii < 0:
            break
        score.set_tonality(MBmusic.tonalities[ii])
    
  
    
    
except:
    
    traceback.print_exc()

finally:
    seq.quit()
    mid.quit()