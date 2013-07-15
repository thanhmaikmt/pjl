import sys
sys.path.append('../MB')

import time
import MBmidi
import MBsetup
import MBmusic


class Band:
    
    def __init__(self):
        
        mid = MBmidi.MidiEngine()
        
        midi_out_dev = mid.open_midi_out(MBsetup.MIDI_OUT_NAMES)
            
        seq = MBmusic.Sequencer()
        # MetroNome
        accent = MBmusic.NoteOn(61, 100)
        weak = MBmusic.NoteOn(60, 80)
        metro_inst = midi_out_dev.allocate_channel(9)
        
        self.metro = MBmusic.Metro(0, 4,seq, metro_inst, accent, weak) 
    
        self.bass_inst = midi_out_dev.allocate_channel(1)  
        # Vamp
        self.vamp_inst = midi_out_dev.allocate_channel(0)
        
        
        self.solo_inst = midi_out_dev.allocate_channel(2)
        self.solo_player=MBmusic.Player(self.solo_inst)
 
        self.seq=seq
        self.mid=mid
        
    def start(self):
        self.seq.start()
        
    def quit(self):
        
        self.seq.quit()
        print ' Stopping midi engine '  
        self.mid.quit()
           
    
class Session:
    
    def __init__(self,name,seq):
        self.out=open(name,"w")
        self.seq=seq
        
        print self.out
        
    def record(self,addr,data):
        print " RECORDING "
#        stamp=time.time()
        strng=str(self.seq.beat)+"|"+addr+"|"+str(data)+"\n"
        self.out.write(strng)
    
    def close(self):
        self.out.close()
            
    
band=Band()

session=Session("SessionTest.dat",band.seq)

# Score
beats_per_bar=4
bars_per_section=1
key=MBmusic.G
start=0

score = MBmusic.Score(bars_per_section,beats_per_bar,key)
score.set_tonality(MBmusic.I, 0)

import MBmapper
mapper=MBmapper.Mapper(band.seq,score,band.vamp_inst,band.solo_inst)
#client=Client(band,session)


band.start()

drivers=[]
    
try:    
    import oscdriver
    addr=MBsetup.get_osc_ip()
    osc_driver=oscdriver.OSCDriver(addr,mapper.map,session)
    osc_driver.run()
    drivers.append(osc_driver)
    
    import os
    os.system("/usr/local/bin/python pg_musicbox.py")
    
            
    xxx=raw_input(" HIT CR ")
    session.close()  
    
except:
    import traceback
    #print e.get_message()
    traceback.print_exc()
    

finally:
    
    print 'Stopping drivers: '  
    band.quit()
    for drv in drivers:
        print drv
        drv.stop()
        
        
        
    
    print 'Thats it ! '  
    import sys
    sys.exit(0)
 

