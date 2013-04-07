
from music import *
from pjlmidi import *
  

  
if __name__ == "__main__":    
    
    mid=MidiEngine()


    midi_out=mid.open_midi_out(MIDI_OUT_NAME)
    
    inst=Instrument(midi_out,1)
    

    phrase=Phrase(period=4)
    
    
    for i in range(12):
        phrase.add(i/3.0,NoteOn(60+i,90))
        phrase.add((i+1)/3.0,NoteOff(60))
    
    class Repeater:
        
        def __init__(self,start,period,phrase,inst,seq):
            self.time=start
            self.player=Player(inst)
            self.period=phrase.period
            seq.add(start,self)
            self.seq=seq
            
        def fire(self):
            print " Send "  
            self.seq.schedule_at(self.time,phrase,self.player)
            self.time+=self.period
            self.seq.add(self.time,self)
          
   
         
    seq=Sequencer()
    r=Repeater(0,4,phrase,inst,seq)
    
    seq.start()
    


        
    