
from music import *
from pjlmidi import *
from players import *

if __name__ == "__main__":    
    

    mid= MidiEngine()
    
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
  
    seq=Sequencer(ticks_per_beat=1000,bpm=520)
    mid.set_midi_out(midi_out_id)
    
#  MetroNome
    inst=Instrument(mid.midi_out,9)
    accent=NoteOn(61,100)
    weak=NoteOn(60,80)
    mess=Metro(0,seq,inst,accent,weak)
    
    
 
    seq.start()
    


        
    