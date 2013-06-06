
import MBmusic
import MBmidi
import MBsetup 
import MBoscserver
import MBmapper
import math
import sys
import traceback
import players


do_metro=True
do_bass=True
do_vamp=True
do_solo=True

try:
    mid = MBmidi.MidiEngine()
    
    midi_out_dev = mid.open_midi_out(MBsetup.MIDI_OUT_NAMES)
        
    seq = MBmusic.Sequencer()
    
    # Score
    beats_per_bar=4
    bars_per_section=1
    key=MBmusic.G
    start=0
    
    score = MBmusic.Score(bars_per_section,beats_per_bar,key)
    score.set_tonality(MBmusic.I, 0)
  
    mapper={}
      
    if do_metro:
        # MetroNome
        accent = MBmusic.NoteOn(61, 100)
        weak = MBmusic.NoteOn(60, 80)
        metro_inst = midi_out_dev.allocate_channel(9)
        
        metro = MBmusic.Metro(0, 4,seq, metro_inst, accent, weak) 
        
    # bass line

    if do_bass:
        class BassData:
            
            def __init__(self):
                self.times =   [0.0,  1., 2.0, 3.0]
                self.vels =    [100,  70,  90,  70]                 
                self.durs =    [0.6, 0.4, 0.4 , 0.4]
                self.pattern=  [0,   0,  0,  0]
    
    
        bass_inst = midi_out_dev.allocate_channel(1)  
        bass_player = MBmusic.BassPlayer(seq, bass_inst, score,30,48)
        bass_data=BassData()
        bass_factory=MBmusic.GrooverFactory(seq,bass_data,bass_player)
        MBmusic.Repeater(0, 4, seq, bass_factory) 
        
        

    if do_vamp:
        # Vamp
            vamp_inst = midi_out_dev.allocate_channel(0)
      
        
        
            vamp_player = MBmusic.ChordPlayer(seq, vamp_inst, score, 60,[0,1,2])
        
            class VampData:
                
                def __init__(self):
                    self.times = [0.5, 1.5, 2.0]
                    self.vels =  [80,  70,  70]                 
                    self.durs =  [0.6, 0.4, 0.4]
               
                    
            vamp_data=VampData()
            factory=MBmusic.GrooverFactory(seq,vamp_data,vamp_player)   
            MBmusic.Repeater(0, 4, seq, factory) 
    
    
    if do_solo:
        solo_inst=midi_out_dev.allocate_channel(2)
        solo_player=players.MelodyPlayer(solo_inst)
        m=MBmapper.SimpleMapper(solo_player)
        mapper['melody']=m.map
            
            #solo_player=MBmusic.Player(solo_inst)
    # ready to go
    

    seq.start()
    
        
           
    #client=Client(seq)
    
    
    # mapper=MBmapper.Mapper(seq,score,vamp_inst,solo_inst)
    
    drivers=[]
    
    
    addr=MBsetup.get_osc_ip()
    osc_driver=MBoscserver.Server(addr,mapper,None)
    osc_driver.run()
    drivers.append(osc_driver)
    
   
    
    
    #import os
    #os.system("python ../FrontEnds/midi_ui.py")
    #os.system("/usr/local/bin/python ../FrontEnds/pg_ui.py")
    
            
    xxx=raw_input(" HIT CR ")
      
    
except:
    
    #print e.get_message()
    traceback.print_exc()
    

finally:
    
    print 'Stopping drivers: '  
   
    for drv in drivers:
        print drv
        drv.quit()
        
        
        
    seq.quit()
    print ' Stopping midi engine '  
    mid.quit()
    
    print 'Thats it ! '  
    
    sys.exit(0)
 
