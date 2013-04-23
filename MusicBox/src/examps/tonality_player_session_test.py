
import music
from pjlmidi import *
from mbconstants import  *
import oscdriver
import math
import sys
import traceback

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
    
    
    class Session:
        
        def __init__(self,name):
            self.out=open(name,"w")
            
        def record(self,addr,data):
            stamp=time.time()
            str=str(time)+addr+str(data)+"\n"
            self.out.write(str)
        
        def close(self):
            self.out.close()
                
        
    class SessionPlayer:
        
        def __init__(self,name,seq,client):
            self.fin=open(name,"r")
            self.seq=seq
            self.client=client
            
        def start(self):
            self.start=time.time()
            self.toff=self.start-time
            time,self.addr,self.data=self.next()
            tnext=time+self.toff
            seq.add(tnext,self)
            
        def fire(self):
            self.client.handle(self.addr,self.data)
            self.next()
            time,self.addr,self.data=self.next()
            #  time+toff=start
            tnext=time+self.toff
            seq.add(tnext,self)
            
             
        def next(self):
            line=self.fin.readline()
            toks=line.split()
            tnext=float(toks[0])
            addr=toks[1]
            data=[]
            for x in toks[2:]:
                data.append(float(x))
            
            return time,addr,data
        
    class ChordPlayer:
        
        def __init__(self):
            self.pitches=[]
            self.template=[0,2,4,6]
        
        def play(self,toks,data):
#           print "chord",toks,data
            
            if toks == "xy":
                y=int(float(data[0])*127)
                x=int(float(data[1])*127)
                vamp_inst.set_volume(y)
                return
            

            for pitch in self.pitches:
                vamp_inst.note_off(pitch)
                
            self.pitches=[]
                                        
            inversion=int(toks[1])     #   TODO
            
            vel=int(float(data[0])*127)
            if vel == 0:
                return
            
        
            tonality=score.get_tonality()
            
            
            for p in range(len(self.template)):
                self.pitches.append(tonality.get_note_of_chord(self.template[p],score.key))
                vamp_inst.note_on(p,vel)
                self.pitches.append(p)

        #  Play notes (shift up +12 if pitch is too low)     
#            for p in self.pitches:
#                while p < self.lowest:
#                    p += 12
#                

       
    class Client:
        
        def __init__(self):
            self.map={"melody":self.melody,
                      "tonality":self.tonality,
                      "chordNote":self.chordNote,
                      "chord":self.chord}
            self.chord_player=ChordPlayer()
            
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
            
            if toks == 'xy':
                x=int(float(data[1])*127)
                y=int(float(data[0])*127)
                print " melody xy",x,y
                return
            
            val=float(data[0])
            
#            assert len(toks) >1
             
            i=int(toks)
            
            print val,i
            vel=int(val*127)       
            pitch=score.get_tonality().get_note_of_scale(i,score.key)+36
            #print "play",i,vel
            
            if vel != 0:
                solo_inst.note_on(pitch,vel)
            else:
                # schedule the note off
                playable = music.Playable(music.NoteOff(pitch), solo_player)
                seq.add_after(.1, playable)
            
    client=Client()
    
    
    drivers=[]
    if False:
        osc_driver=oscdriver.OSCDriver(client)
        osc_driver.run()
        drivers.append(osc_driver)
    
    # respond to a key without the need to press enter


    if True:
        import pgdriver
        pg_driver=pgdriver.PGDriver(client)
        pg_driver.start()
        drivers.append(pg_driver)
        
    xxx=raw_input(" HIT CR ")
      
    
except MidiError as e:
    
    print e.get_message()
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
 
