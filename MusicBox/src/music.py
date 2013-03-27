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
    
    """
    A Message extends an event with a Player.
    The player must be able to send the message of the event
    The event.tick is used by the Sequencer to schedule the message 
    """
    def __init__(self,tick):
        self.tick=tick
        
#    def fire(self):
#        print (self)," Fired "


class MessageEvent(Event):
    
    """
    A Message extends an event with a Player.
    The player must be able to send the message of the event
    The event.tick is used by the Sequencer to schedule the message 
    """
    def __init__(self,tick,mess):
        Event.__init__(self, tick)
        self.mess=mess

class PlayerEvent(MessageEvent):
    
    """
    A Message extends an event with a Player.
    The player must be able to send the message of the event
    The event.tick is used by the Sequencer to schedule the message 
    """
    def __init__(self,tick,mess,player):
        MessageEvent.__init__(self, tick,mess)
        self.player=player

        
    def fire(self):
        self.player.play(self.mess)

    
class Phrase:
    """
    Is a list of Events
    """
    def __init__(self):
        self.list=linkedlist.OrderedLinkedList()
        
        
    def add(self,tick,mess):
        self.list.insert(MessageEvent(tick,mess))
 
         
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
            if node.tick < start:
                continue
            if node.tick > to:
                break
            sequencer.add(PlayerEvent(node.tick,node.data.mess,self.player))
            
  

class Sequencer:
    
    """
    Plays a sequence of messages
    Delegates the timing to an engine which
    must call play_events_at(at) with at incrementing each call
    """
    
    def __init__(self,ticks_per_beat,bpm):
        
        self.sequence=linkedlist.OrderedLinkedList()        
        self.sequence.insert(Event(-1))
        self.sequence.insert(Event(sys.maxint))
        self.engine=Engine(bpm,ticks_per_beat,self.play_events_at)
        self.tick=0
        self.ticks_per_beat=ticks_per_beat
        
        # self.prev is last event to be played
        self.prev=self.sequence.head
        #self.next=self.prev.next
        
        # next should be OK providing we have an end event in the sequence

    def tickAtBeat(self,beat):
        return int(beat*self.ticks_per_beat)
    
    def add(self,event):
        
        """
        event must have a int tick field
        event must have a mess must implement send()
        """
        
        self.sequence.insert(event)
      
        
          
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
        if self.prev.next.tick > at:
            return
        
        # catch up by skipping missed events
        while self.prev.next.tick < at:
            self.prev=self.prev.next
        
        while self.prev.next.tick  == at:
            self.prev=self.prev.next
            self.prev.data.fire()




class Player:
        
    def __init__(self,inst):
        self.inst=inst
        
    def play(self,mess):
        print (mess)   
        mess.send(self.inst)
        
        
        
class NoteOn:
        
    def __init__(self,pitch,vel):
        self.pitch=pitch
        self.vel=vel
        
    def send(self,inst):
        inst.note_on(self.pitch,self.vel)
        
        
class NoteOff:
        
    def __init__(self,pitch,vel=0):
        self.pitch=pitch
        self.vel=vel
        
    def send(self,inst):
        inst.note_off(self.pitch,self.vel)
        
