import threading
import engine




class Sequencer:
    
    def __init__(self):
        self.sequences=[]
        ticks_per_beat=1
        bpm=60

        self.engine=engine.Engine(bpm,ticks_per_beat,self.play_events_at)
  
  
    def start(self):
        self.engine.start()
                  
    def play_events_at(self,at):
        
        for s in self.sequences:
            s.play_events_at(at)
                
    def add_sequence(self,seq):
        """
        seq must implement play_events_at(at)
        """
        self.sequences.append(seq)
        
            
        
        
if __name__ == "__main__":
    # test code
    #  create PyMidi to initialize misi system.
    import pymidi
    mid=pymidi.PyMidi()

    
    # print devicess
    mid.print_device_info()
    
    # define input and output channels
    # adjust these for hardware reported by above
    mid.set_midi_out(5)
    
    #
    #  simplest possible sequence
    class Sequence:
                  
        def play_events_at(self,tick):
            print tick


    seq=Sequence()
    
    sequencer=Sequencer()
    
    sequencer.add_sequence(seq)
    
    sequencer.start()