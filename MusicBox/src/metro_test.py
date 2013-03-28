
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
    

  
    class Metro:
        
        def __init__(self,start,seq,inst,note_accent,note_weak):
            self._time=start
            seq.add(start,self)
            self.seq=seq
            self.accent=note_accent
            self.weak=note_weak
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
            self._time+=1
            seq.add(self._time,self)
             #TODO delete etc.....
            
        
    seq=Sequencer(ticks_per_beat=1000,bpm=520)
    accent=NoteOn(61,100)
    weak=NoteOn(60,80)
    mess=Metro(0,seq,inst,accent,weak) 
    seq.start()
    


        
    