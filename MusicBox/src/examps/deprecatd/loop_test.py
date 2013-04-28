
import music 
import MBmidi
import MB
  

  
if __name__ == "__main__":    
    
    mid=MBmidi.MidiEngine()


    midi_out=mid.open_midi_out(MB.MIDI_OUT_NAMES)
    
    inst=MBmidi.Instrument(midi_out.out,1)
    

    phrase=music.Phrase(period=4)
    
    
    for i in range(12):
        phrase.add(i/3.0,music.NoteOn(60+i,90))
        phrase.add((i+1)/3.0,music.NoteOff(60))
    
    class Repeater:
        
        def __init__(self,start,period,phrase,inst,seq):
            self.time=start
            self.player=music.Player(inst)
            self.period=phrase.period
            seq.schedule(start,self)
            self.seq=seq
            
        def fire(self):
            print " Send "  
            self.seq.schedule_phrase(self.time,phrase,self.player)
            self.time+=self.period
            self.seq.schedule(self.time,self)
          
   
         
    seq=music.Sequencer()
    r=Repeater(0,4,phrase,inst,seq)
    
    seq.start()
    


        
    