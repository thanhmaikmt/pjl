import sys
sys.path.append('../../../MusicBox/src/MB')
import MBmidi
import MBmusic
import atexit
import numpy
import time


SAVE_TO_FILE=False  

if SAVE_TO_FILE:
    import midi
    class SaveMidi:
    
        def __init__(self):
            # Instantiate a MIDI Pattern (contains a list of tracks)
            self.pattern = midi.Pattern()
            # Instantiate a MIDI Track (contains a list of MIDI events)
            self.track = midi.Track()
            # Append the track to the pattern
            self.pattern.append(self.track)
            self.fout=open("BPM.txt","w")
            atexit.register(self.quit)
       
        def process(self,bpm,t,val):
            
            if bpm<30 or bpm >180:
                return
            
            line=str(t)+" "+str(bpm)+"\n"
            self.fout.write(line)
            tick=int(t*2604)
            pitch=max(0,min(int(bpm),127))
            
            # Instantiate a MIDI note on event, append it to the track                      
            on = midi.NoteOnEvent(tick=tick, velocity=100, pitch=pitch)
            self.track.append(on)
            # Instantiate a MIDI note off event, append it to the track                     
            off = midi.NoteOffEvent(tick=tick+1, pitch=pitch)
            self.track.append(off)
            # Add the end of track event, append it to the track                            
            eot = midi.EndOfTrackEvent(tick=1)
            self.track.append(eot)
            
        def quit(self):
                                                                  
            print "QUITING SAVEMIDI "
            # Save the pattern to disk                                                      
            midi.write_midifile("example.mid", self.pattern)
            self.fout.close()

 
        

class PingClient:
    
    def __init__(self):
        
        self.average=60.0
        
        self.n_pad=10
        self.pad_buf=numpy.zeros(self.n_pad,dtype='i')
        self.pad_ptr=0
        self.mid=MBmidi.MidiEngine()
    
        midi_out=self.mid.open_midi_out(["to ARGO Appli Fluidsynth v9 1","Synth input port (Qsynth1:0)","IAC Driver IAC Bus 1"])
                  
        self.inst=MBmidi.Instrument(midi_out.out,0)  
        
#         10 music box
#   11 anny likes
        # 13 xylo
        self.inst.set_instrument(11)
        self.inst.set_reverb(127)
        
        
        self.inst_pad=MBmidi.Instrument(midi_out.out,1)  
        self.inst_pad.set_instrument(89)
        self.inst_pad.set_reverb(127)
        
        
        self.inst_drone=MBmidi.Instrument(midi_out.out,2)  
        self.inst_drone.set_instrument(51)
        
#         self.inst_drone.set_reverb(127)  
#         self.inst_drone.note_on(36,10)
#         self.inst_drone.note_on(48,4)
#         self.inst_drone.note_on(55,3)
        
        self.pitchLast=None
        
        atexit.register(self.quit)
        
        self.scale=[0,2,4,7,9]
        
        self.fact1=0.85
        self.fact2=1.0-self.fact1
        self.rptCnt=3
        self.cnt=0
        
    def toScale(self,i):
        
        irem=i%5
        ifloor=i/5
        
        ipitch=12*ifloor+self.scale[irem]
        
        return max(min(108,ipitch),12)
        
        
    def process(self,bpm,t,val):
        
        
        self.cnt +=1
        if self.cnt < 10:
            return
        
        print bpm
        self.average = self.average*self.fact1+self.fact2*bpm
        
        dval = bpm-self.average
        
        print "val ,av" ,dval,self.average
        
        ii=int(25+dval*.8)
        
        if (ii < 0):
             return

        ibpm=self.toScale(ii)
        pit2=self.toScale(ii-10)
        
        vel=45
        # print bpm,ibpm,vel
        
        
        if self.pitchLast != None:
            
            self.inst.note_off(self.pitchLast)
        
            if self.pitchLast == ibpm:
                self.rptCnt+=1
            else:
                self.rptCnt=1
            
        vel = int(vel * 1.0/self.rptCnt)
        
        vel=int(max(0,min(vel,120)))
        
#         print vel,self.rptCnt
        
        self.inst.note_on(ibpm,vel)
        
        
        self.pad_ptr=(self.pad_ptr+1)%self.n_pad
        pitNext=self.pad_buf[self.pad_ptr]
        
        if pitNext > 0:
            self.inst_pad.note_off(pitNext)
        
        self.inst_pad.note_on(pit2,10)
        self.pad_buf[self.pad_ptr]=pit2
        
        self.pitchLast=ibpm
    
    def quit(self):
        
        print " Shutting down midi "
        
        self.inst_pad.all_note_off()
        self.inst_drone.all_note_off()   
        time.sleep(2)  
        self.mid.quit()

class OnEvent:
    
    
    def __init__(self,inst,pitch,vel):
        self.inst=inst
        self.pitch=pitch
        self.vel=vel
        
    def fire(self,tt):
        self.inst.note_on(self.pitch,self.vel)
        
class OffEvent:
    
    
    def __init__(self,inst,pitch):
        self.inst=inst
        self.pitch=pitch

        
    def fire(self,tt):
        self.inst.note_off(self.pitch)
        
class PingClient2:
    
    PENTA,MELODIC_MINOR=range(2)
    
    def __init__(self):
        
        self.average=60.0
        
        self.n_pad=10
        self.pad_buf=numpy.zeros(self.n_pad,dtype='i')
        self.pad_ptr=0
        self.mid=MBmidi.MidiEngine()
       # self.seq=MBmusic.SequencerBPM()
        # self.seq.start()
    
        midi_out=self.mid.open_midi_out(["to ARGO Appli Fluidsynth v9 1","Synth input port (Qsynth1:0)","IAC Driver IAC Bus 1"])
                  
        self.inst=MBmidi.Instrument(midi_out.out,0)  
        
#         10 music box
#   11 anny likes
        # 13 xylo
        self.inst.set_instrument(11)
        self.inst.set_reverb(127)
        
        
        self.inst_pad=MBmidi.Instrument(midi_out.out,1)  
        self.inst_pad.set_instrument(89)
        self.inst_pad.set_reverb(127)
        
        
        self.inst_drone=MBmidi.Instrument(midi_out.out,2)  
        self.inst_drone.set_instrument(51)
        
#         self.inst_drone.set_reverb(127)  
#         self.inst_drone.note_on(36,10)
#         self.inst_drone.note_on(48,4)
#         self.inst_drone.note_on(55,3)
        
        self.pitchLast=None
        
        atexit.register(self.quit)
        
        scale=PingClient2.PENTA
        
        if scale == PingClient2.PENTA:
            self.scale=[0,2,4,7,9]
            self.scale_drone=[0,4,7,9,12,14,16,19,21,24,26,28,31,33,36]
            self.scale_root=0
        else:
            self.scale=[0,2,3,5,7,8,11]
            self.scale_drone=[0,7,9,12,14,15,17,19,24,26,27,29,31,32,35,36,38]
            self.scale_root=12
        
        self.nScale=len(self.scale)
        
        
        
        self.fact1=0.85
        self.fact2=1.0-self.fact1
        self.rptCnt=3
        self.cnt=0
        self.playing=numpy.zeros(127,dtype='i')
        
    def toScale(self,i):
        
        irem=i%self.nScale
        ifloor=i/self.nScale
        
        ipitch=self.scale_root+12*ifloor+self.scale[irem]
        
        return max(min(108,ipitch),12)
        
    def toScaleDrone(self,i):
        
        i=max(i,0)
        i=i%len(self.scale_drone)
        ipitch=self.scale_root+36+self.scale_drone[i]
        
        return max(min(108,ipitch),12)
   
        
    def process(self,bpm,t,val):
        
        self.cnt +=1
        if self.cnt < 4:
            return
        
        print bpm
        self.average = self.average*self.fact1+self.fact2*bpm
        
        dval = bpm-self.average
        
        print "val ,av" ,dval,self.average
        
        ii=int(25+dval*.8)
        
        if (ii < 0):
             return

        ibpm=self.toScale(ii)
        pit2=self.toScaleDrone(ii-2)
        
        vel=55
        # print bpm,ibpm,vel
        
        
        if self.pitchLast != None:
            
            self.inst.note_off(self.pitchLast)
        
            if self.pitchLast == ibpm:
                self.rptCnt+=1
            else:
                self.rptCnt=2
            
        vel = int(vel * 2.5/self.rptCnt)
        
        vel=int(max(0,min(vel,120)))
        
#         print vel,self.rptCnt
        
      #  tt=self.seq.get_stamp()
        # self.seq.schedule(tt+0.1,OnEvent(self.inst,ibpm,vel))
        self.inst.note_on(ibpm,vel)
        self.pitchLast=ibpm
      
        
        self.pad_ptr=(self.pad_ptr+1)%self.n_pad
        pitNext=self.pad_buf[self.pad_ptr]
        
    
        if pitNext > 0:
            self.inst_pad.note_off(pitNext)
            self.playing[pitNext]=0
            self.pad_buf[self.pad_ptr]=0
            
        if self.playing[pit2]:
            return
        
        self.inst_pad.note_on(pit2,10)
        self.pad_buf[self.pad_ptr]=pit2
        self.playing[pit2]=1
        
      
    def quit(self):
        
        print " Shutting down midi "
        
        for i in range(127):
            self.inst_pad.note_off(i)
        
        if self.pitchLast != None:
            
            self.inst.note_off(self.pitchLast)
        
        self.inst_pad.all_note_off()
        self.inst_drone.all_note_off()   
        time.sleep(2)  
     #   self.seq.quit()
        self.mid.quit()
