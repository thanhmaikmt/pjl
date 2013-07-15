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

    
class SessionPlayer:
    
    def __init__(self,name,seq,mapper):
        self.fin=open(name,"r")
        self.seq=seq
        self.mapper=mapper
        self.name=name
        
    def start(self):
        self.start=self.seq.beat
        self.schedule_next()
        
    def fire(self,beat):
    
        toks=self.addr.split('/')
        
        if len(toks) < 3:
            return
        
        func=self.mapper.get(toks[2])
        
        if func != None:
            func(toks[3:],self.data)
        else:
            print " No musicbox handler for:", self.addr
#        print addr,data
        
        self.schedule_next()
        
         
    def schedule_next(self):
        line=self.fin.readline()
        if line:
            toks=line.split('|')
            tnext=float(toks[0])
            self.addr=toks[1]
            if len(toks)>=3:
                self.data=eval(toks[2])
            else:
                self.data=None
            self.seq.schedule(tnext,self)
        else:
            print "end of file: ", self.name
        
            
        
    
band=Band()


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


session=SessionPlayer("SessionTest.dat",band.seq,mapper.map)
session.start()
band.start()

    
try:    
#    import oscdriver
#    addr=MBsetup.get_osc_ip()
#    osc_driver=oscdriver.OSCDriver(addr,mapper.map,session)
#    osc_driver.run()
#    drivers.append(osc_driver)
#    
#    import os
#    os.system("/usr/local/bin/python pg_musicbox.py")
#    
            
    xxx=raw_input(" HIT CR ")
    session.close()  
    
except:
    import traceback
    #print e.get_message()
    traceback.print_exc()
    

finally:
    
    print 'Stopping drivers: '  
    band.quit()
  
        
        
        
    
    print 'Thats it ! '  
    import sys
    sys.exit(0)
 

