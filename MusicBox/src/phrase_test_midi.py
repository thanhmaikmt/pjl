
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
    

    phrase=Phrase()
    phrase.add(0,NoteOn(60,90))
    phrase.add(1,NoteOff(60))
    phrase.add(3,NoteOn(61,90))
    phrase.add(4,NoteOff(61))    
    phrase.add(3,NoteOn(66,90))
    phrase.add(4,NoteOff(66))
    phrase.add(2,NoteOn(60,90))
    phrase.add(5,NoteOff(60))
   
    
   
         
    ticks_per_beat=2*2*3*5
    seq=Sequencer(ticks_per_beat=ticks_per_beat,bpm=120)
    seq.schedule_at(0,phrase,Player(inst))
    
    seq.start()
    


        
    