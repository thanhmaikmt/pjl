
from music import *
from midi import *
  

  
if __name__ == "__main__":    
    
    mid=Engine()

    # print devicess
    devs=mid.device_info()
    
    midi_out_id=-1
    
    for dev in devs:
                
        if dev.output:
            print dev.id,dev.name
            if "to ARGO Appli Fluidsynth v9 1"in dev.name:
                midi_out_id=dev.id
                break
            
            if  "MusicBox" in dev.name:
                midi_out_id=dev.id
          
            
    print "using id:",devs[midi_out_id].name
    
    mid.set_midi_out(midi_out_id)
    inst=Instrument(mid.midi_out,9)
    


    class Context(Event):
        
        def __init__(self,time,seq,inst):
            self.time=seq.time
            Event.__init__(self, time)
            seq.add(self)
            self.seq=seq
            self.context
            
            self.beats_per_bar=4
            self.bars_per_section=4
            scale=[0,3,4,6,8,9,11]    
            key=40  
            triad=[0,3,5]  
            self.chords.append(Tonality(key,scale,triad,0))    
            self.chord1=Tonality(key,scale,triad,0)    
                
                
        def fire(self):
            print " Context fire at ",seq.time
            
            if self.count %self.beats_per_bar == 0:
                self.accent.send(inst)
            else:
                self.weak.send(inst)
            
            self.count+=1
            self.time+=seq.ticks_per_beat
            seq.add(self)
             #TODO delete etc.....
        
        
        
  
    class BassLine(Event):
        
        def __init__(self,time,seq,inst,context):
            self.time=seq.time
            Event.__init__(self, time)
            seq.add(self)
            self.seq=seq
            self.context
            self.pattern=[0,1,2,3]
            self.count=0
            self.beats_per_bar=4
            self.inst=inst
                    
        def fire(self):
            print " Send "
            if self.count %self.beats_per_bar == 0:
                self.accent.send(inst)
            else:
                self.weak.send(inst)
            
            self.count+=1
            self.time+=seq.ticks_per_beat
            seq.add(self)
             #TODO delete etc.....
            
        
        
    
    
    seq=Sequencer(ticks_per_beat=1,bpm=120)
    accent=NoteOn(61,100)
    weak=NoteOn(60,80)
    mess=Metro(0,seq,inst,accent,weak) 
    seq.start()
    


        
    