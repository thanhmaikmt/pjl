import linkedlist
import sys
import time
from threading import Thread

SLEEP_TIME=0.001    # time to yield in engine event loop

class Engine(Thread):


    """
    Engine calls a call_back every tick
      yields using sleep to allow multithreading
    """


    def __init__(self,bpm,ticks_per_beat,call_back=None,idle=None):
        
        self.dt=60.0/bpm/ticks_per_beat
        self.call_back=call_back
        self.idle=idle
        Thread.__init__(self)
        
    def run(self):
        self.running=True
        tnext=tnow=time.time()
        tick=0
    
        while self.running:
            
            # spin until next tick
            while tnow < tnext:
                # yeild to other threads
                time.sleep(SLEEP_TIME) 
                tnow=time.time()       
            
            self.call_back(tick)
            tnext+=self.dt
            tick+=1
            
            

class Event:
    
    def __init__(self,tick,message):
        self.tick=tick
        self.message=message
        
    def __gt__(self,a):
        return self.tick > a.tick
    
    def __lt__(self,a):
        return self.tick < a.tick
    
    def __eq__(self,a):
        return self.tick == a.tick
        
        

class Message(Event):
    
    """
    A Message extends an event with a Player.
    The player must be able to send the message of the event
    The event.tick is used by the Sequencer to schedule the message 
    """
    def __init__(self,event,player):
        self.player=player
        Event.__init__(self,event.tick,event.message)
        
    def send(self):
        self.player.play(self.message)
    
    
class Phrase:
    """
    Is a list of Events
    """
    def __init__(self):
        self.list=linkedlist.OrderedLinkedList()
        
        
    def add(self,tick,message):
        self.list.insert(Event(tick,message))
 
         
    def __iter__(self):
        return self.list.__iter__()

        
  
class Scheduler:
    
    """
    Adds messages to the sequencer to play a segment of a phrase
    using a player.
    """

    def __init__(self,phrase,player):
        self.phrase=phrase   
        self.player=player   
        
    def schedule(self,start,to,sequencer):
        
        for node in self.phrase:
            if node.data.tick < start:
                continue
            if node.data.tick > to:
                break
            sequencer.add(Message(node.data,self.player))
            
  

class Sequencer:
    
    """
    Plays a sequence of messages
    Delegates the timing to an engine which
    must call play_events_at(at) with at incrementing each call
    """
    
    def __init__(self):
        self.sequence=linkedlist.OrderedLinkedList()
        
        self.sequence.insert(Message(Event(-1,None),None))
        self.sequence.insert(Message(Event(sys.maxint,None),None))
        ticks_per_beat=1
        bpm=60
        self.engine=Engine(bpm,ticks_per_beat,self.play_events_at)
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
        """
        start the engine which should call play_events_at(at)
        """
        self.engine.start()
                  
    def play_events_at(self,at):
        
        """
        Play messages and advance the time.
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
