
from music import *
from pjlmidi import *
from players import *
import priority
from setup import  *
  
if __name__ == "__main__":    
    
    
    


    class Tonality:
        
        """
        Key is a refence midi note number defines relative pitch
        (lowest note of this tonality)
        scale is the set of notes to be used.
        chord is indices of note in scale that make up the chord off set by root.
        
        e.g.
        
        key+scale[i]                  plays to scale
        key+scale[root+chord[i]]      plays arpegio 
        """
         
        def __init__(self,key,scale,chord,root):
            self.key=key
            self.chord=chord
            self.root=root
            self.scale=scale
            
            
        def get_note_of_chord(self,i):
            
            assert i < len(self.chord)
            ii=self.root+self.chord[i]
            assert ii < len(self.scale)
            return self.key+self.scale[ii]
            
            
            
    class Score:
        
        def __init__(self,start,seq):
            self.beat=start-1
            self.beats_per_bar=4 
            self.bars_per_section=4
            self.beat_one_time=-4
            
            scale=[0,2,4,5,7,9,11]    
            
            for oct in range(2):
                for n in range(7):
                    scale.append(scale[n]+(oct+1)*12)
       
#            print scale
            
            key=36  
            triad=[0,2,4,2 ]  
            
            self.tonalities=[]
            self.tonalities.append(Tonality(key,scale,triad,7))
            self.tonalities.append(Tonality(key,scale,triad,5))
            self.tonalities.append(Tonality(key,scale,triad,3))
            self.tonalities.append(Tonality(key,scale,triad,4))    

            seq.add(start,self)
            self.seq=seq
            
        def get_tonality(self):
            bar=int(self.beat/self.beats_per_bar)
            return self.tonalities[bar%self.bars_per_section]
 
        def fire(self):
            #print "Score fire "
            self.beat+=1
            self.seq.add(self.beat+1,self,priority.score)
            if self.beat%self.beats_per_bar == 0: 
                self.beat_one_time=self.beat
            
        def get_count(self):
            return self.beat%self.beats_per_bar      
        
        def get_time(self):
            return seq.beat
            
    class BassLine:
        
        def __init__(self,start,seq,inst,score):
            seq.add(start,self)
            self.seq=seq
            self.score=score
            self.pattern=[0,1,2,3]
            self.pulse=[120,90,100,85]
            self.times=[1,1,1,1]
            self.n=4
            self.inst=inst
            self.pending=None
                
        def fire(self):
            #print " Bass.fire"
    
            
            if self.pending != None:
                self.inst.note_off(self.pending)
            
            tonality=self.score.get_tonality()
            count=self.score.get_count()
            pitch=tonality.get_note_of_chord(self.pattern[count])
            self.pending=pitch
            velocity=self.pulse[count]
            
            #print count,pitch,velocity
            self.inst.note_on(pitch, velocity)
            
            seq.add(self.score.seq.beat +self.times[count],self)
            
            self.pending=pitch

        
    class VampLine:
        
        def __init__(self,start,seq,inst,score,lowest):
            self.seq=seq
            self.score=score
            #self.pattern=[0,1,2,3]
            self.pulse=[80,70,70]
                             
            period=4
            self.deltas=[0.5,1.0,0.5]
            self.durs=[0.6,0.4,0.4]
            self.n=3
            self.period=4
            self.inst=inst
            self.lowest=lowest
            self.player=Player(inst)

            Repeater(start,period,seq,Groove,deltas=self.deltas,player=self)
            
           # seq.add(start+self.times[0],self)
            
            
            
            
        def play_count(self,count):
            #print " Vamp.fire"
            
            tonality=self.score.get_tonality()

            
            dur=self.durs[count]
            velocity=self.pulse[count]
                
            pitch=[]
            for p in range(self.n):
                pitch.append(tonality.get_note_of_chord(p))

            # TODO Voicings
            
            #print count,pitch,velocity
            
            for p in pitch:
                while p < self.lowest:
                    p+=12
                    
                self.inst.note_on(p, velocity)
                playable=Playable(NoteOff(p),self.player)
                seq.add_after(dur,playable)
                
                        
        
        
    
    mid=MidiEngine()

    midi_out=mid.open_midi_out(MIDI_OUT_NAME)
    
    
    seq=Sequencer(ticks_per_beat=2*2*3*5,bpm=100)
    
    # Context
    
    score=Score(0,seq)
    
    
    # MetroNome
    accent=NoteOn(61,100)
    weak=NoteOn(60,80)
    inst=Instrument(midi_out,9)
    
    metro=Metro(0,seq,inst,accent,weak) 
    
    # bass line
    bass_inst=Instrument(midi_out,1)
    
    bass=BassLine(0,seq,bass_inst,score)
    
    
    
    # Vamp
    vamp_inst=Instrument(midi_out,0)
    
    vamp=VampLine(0,seq,vamp_inst,score,60)
    

    seq.start()
    
    xx=raw_input(" Hit CR TO QUIT")

    seq.quit()    
    bass_inst.all_note_off()
    

    mid.quit()


        
    