
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
            
            if "to ARGO Appli Fluidsynth v9 1"in dev.name or "MusicBox" in dev.name:
                midi_out_id=dev.id
          
            
    print "using id:",devs[midi_out_id].name
    
    mid.set_midi_out(midi_out_id)
    inst=Instrument(mid.midi_out,0)
    

    phrase=Phrase()
    phrase.add(0,NoteOn(60,90))
    phrase.add(1,NoteOff(60))
    phrase.add(3,NoteOn(61,90))
    phrase.add(4,NoteOff(61))    
    phrase.add(3,NoteOn(66,90))
    phrase.add(4,NoteOff(66))
    phrase.add(2,NoteOn(60,90))
    phrase.add(5,NoteOff(60))
   
 
    worker=Scheduler(phrase,Player(inst))
        
    seq=Sequencer()
    worker.schedule(0,10,seq)
    
    seq.start()
    


        
    