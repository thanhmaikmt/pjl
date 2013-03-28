
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
    inst=Instrument(mid.midi_out,1)
    

    phrase=Phrase(period=4)
    
    
    for i in range(12):
        phrase.add(i/3.0,NoteOn(60+i,90))
        phrase.add((i+1)/3.0,NoteOff(60))
    
    class Repeater(Event):
        
        def __init__(self,time,period,phrase,inst,seq):
            self.time=time
            Event.__init__(self, time)
            self.scheduler=Scheduler(phrase,Player(inst),seq)
            self.period=phrase.period
        
        def fire(self):
            print " Send "  
            self.scheduler.scheduleAt(seq.time)
            self.time+=self.period
            seq.add(self)
          
   
         
    seq=Sequencer(ticks_per_beat=1,bpm=120)
   
    seq.add(Repeater(0,))
    
    seq.start()
    


        
    