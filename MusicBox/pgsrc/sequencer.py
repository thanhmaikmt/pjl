import threading
import engine
import linkedlist
from phrase import *
import sys



class Sequencer:
    
    def __init__(self):
        self.sequence=linkedlist.OrderedLinkedList()
        
        self.sequence.insert(Message(Event(-1,None),None))
        self.sequence.insert(Message(Event(sys.maxint,None),None))
        ticks_per_beat=1
        bpm=60
        self.engine=engine.Engine(bpm,ticks_per_beat,self.play_events_at)
        self.tick=0
        
        # self.prev is last event to be played
        self.prev=self.sequence.head
        #self.next=self.prev.next
        
        # next should be OK providing we have an end event in the sequence

    def add(self,mess):
        
        """
        mess must have a tick field (imutable)
        mess must implement send()
        """
        
        self.sequence.insert(mess)
        
    def start(self):
        self.engine.start()
                  
    def play_events_at(self,at):
        
        """
    
        """
        print at
        
        # if next event is after at just return
        if self.prev.next.data.tick > at:
            return
        
        # catch up by skipping missed events
        while self.prev.next.data.tick < at:
            self.prev=self.prev.next
        
        while self.prev.next.data.tick  == at:
            self.prev=self.prev.next
            self.prev.data.send()
            
     
        
if __name__ == "__main__":
    # test code
    #  create PyMidi to initialize misi system.
    import pymidi
    mid=pymidi.PyMidi()

    
    # print devicess
    mid.print_device_info()
    
    # define input and output channels
    # adjust these for hardware reported by above
    mid.set_midi_out(1)
    
    #
    #  simplest possible sequence
    class Sequence:
                  
        def play_events_at(self,tick):
            
            note=60+(tick/2)%12
            
            if tick % 2 == 0 :
                mid.midi_out.note_on(note, velocity=100, channel = 1)
            else:
                mid.midi_out.note_off(note, velocity=0, channel = 1)
            #print tick


    seq=Sequence()
    
    sequencer=Sequencer()
    
    sequencer.add_sequence(seq)
    
    sequencer.start()
    
    tt=raw_input("Hit cr to quit:")
    #wait a few secs then halt
    
    mid.cleanup()