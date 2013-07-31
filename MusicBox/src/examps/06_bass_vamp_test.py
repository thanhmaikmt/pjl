import sys
sys.path.append('../MB')


import MBmusic as music
import MBmidi 
import MBsetup


try:
    mid = MBmidi.MidiEngine()
    
    midi_out_dev = mid.open_midi_out(MBsetup.MIDI_OUT_NAMES)
    
    
    seq = music.SequencerBPM(beats_per_sec=4)
    
    # Score
    beats_per_bar=4
    bars_per_section=4
    key=music.G
    start=0
    
    score = music.Score(bars_per_section,beats_per_bar,key)
    score.set_tonality(music.I, 0)
    score.set_tonality(music.vi, 1) 
    score.set_tonality(music.ii, 2)
    score.set_tonality(music.V , 3)
    

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
            self.pattern=  [0,   4,  5,  6]


    bass_inst = midi_out_dev.allocate_channel(1)  
    bass_player = music.BassPlayer(seq, bass_inst, score,43,58)
    bass_data=BassData()
    bass_factory=music.GrooverFactory(seq,bass_data,bass_player)
    music.Repeater(0, 4, seq, bass_factory.create) 
    
    # Vamp
       
    vamp_inst = midi_out_dev.allocate_channel(0)
    vamp = music.ChordPlayer(seq, vamp_inst, score, 60,[0,1,2,3])
 
    class VampData:
        
        def __init__(self):
            self.times = [0.5, 1.5, 2.0]
            self.vels =  [80,  70,  70]                 
            self.durs =  [0.6, 0.4, 0.4]
       
            
   
    vamp_data=VampData()
    
    
    factory=music.GrooverFactory(seq,vamp_data,vamp)   
    
    
    
    music.Repeater(0, 4, seq, factory.create) 
    
    
    
    # ready to go
    
    seq.start()
    
    xx = raw_input(" Hit CR TO QUIT")
    
    seq.quit()
    mid.quit()
    
except MBmidi.MidiError as e:
    import traceback
    traceback.print_stack()
    print e.get_message()

 
