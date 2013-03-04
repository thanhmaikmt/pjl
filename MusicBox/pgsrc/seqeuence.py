

class Seqeuncer:
    
    def __init__(self):
        self.sequences=[]
        
            
    def play_events_at(self,at):
        
        for s in self.sequences:
            s.play_events(at)
                
    def add_sequnce(self,seq):
        self.sequences.append(seq)
        
        