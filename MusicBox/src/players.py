import priority

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
        
#        print " Metro.fire"
    
        if self.count %self.beats_per_bar == 0:
            self.accent.send(self.inst)
        else:
            self.weak.send(self.inst)
        
        self.count+=1
        self._time+=1
        self.seq.add(self._time,self)
        #TODO delete etc.....



class Conductor:

        def __init__(self, start, score, seq):
            self.seq = seq
            self.count = 0
            self.beats_per_bar = 4
    
            self.score = score
       
  
    
        def beat_in_bar(self):
            return self.seq.beat() % self.beats_per_bar

class BassPlayer:
      
    def __init__(self,start,seq,inst,score,conductor):
        self._time=start
        seq.add(start,self)
        self.seq=seq
        self.count=0
        self.beats_per_bar=4
        self.inst=inst
        self.score=score
        self.condcutor=conductor
                   
    def fire(self):
        
        print " Send "
    
        if self.count %self.beats_per_bar == 0:
            self.accent.send(self.inst)
        else:
            self.weak.send(self.inst)
        
        self.count+=1
        self._time+=1
        self.seq.add(self._time,self)
        #TODO delete etc.....
