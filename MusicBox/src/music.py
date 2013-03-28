import linkedlist
import sys
import time
from threading import Thread

SLEEP_TIME=0.001    # time to yield in engine event loop

class Engine(Thread):


    """
    Engine calls a call_back every time
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
            
            # spin until next time
            while tnow < tnext:
                # yeild to other threads
                time.sleep(SLEEP_TIME) 
                tnow=time.time()       
            
            self.call_back(tick)
            tnext+=self.dt
            tick+=1
            
 
#
#class Event:
#    
#    """
#    Base class for timed objects.
#    The event.time is used by the Sequencer to schedule the message.
#    derived classes should implement fire() 
#    """
#    def __init__(self,time):
#        self.time=time
#        
##    def fire(self):
##        print (self)," Fired "
#
#
#class MessageEvent(Event):
#    
#    """
#    A Message extends an event with a message.
#    We can store phrases as a list of messages.
#    """
#    def __init__(self,time,mess):
#        Event.__init__(self, time)
#        self.mess=mess

class Playable:
    
    """
    A PlayerEvent extends a Message with a Player.
    The player must be able to send the message of the event
    The event.time is used by the Sequencer to schedule the message 
    """
    def __init__(self,mess,player):
        self.mess=mess
        self.player=player

        
    def fire(self):
        self.player.play(self.mess)



   

 
class Phrase:
    """
    Is a list of Events
    """
    def __init__(self,period=None):
        self.list=linkedlist.OrderedLinkedList()
        self.period=period
        
    def add(self,time,mess):
        self.list.insert(time,mess)
 
         
    def __iter__(self):
        return self.list.__iter__()

        
 
   

class Sequencer:
    
    """
    Plays a sequence of messages
    Delegates the timing to an engine which
    must call play_events_at(at) with at incrementing each call
    """
    
    def __init__(self,ticks_per_beat=2*2*3*4,bpm=120):
        
        
        self.sequence=linkedlist.OrderedLinkedList()        
        self.sequence.insert(-1,None)
        self.sequence.insert(sys.maxint,None)
        self.engine=Engine(bpm,ticks_per_beat,self._play_events_at)
        self.time=0
        self.ticks_per_beat=ticks_per_beat
        
        # self.prev is last event to be played
        self.prev=self.sequence.head
        #self.next=self.prev.next
        
        # next should be OK providing we have an end event in the sequence

    def _real_to_tick(self,beat):
        return int(beat*self.ticks_per_beat)
   
   
    def schedule_at(self,start,phrase,player):    
        for node in phrase:
            self.add(node.time+start,Playable(node.data,player))
            
   
    def add(self,time,event):
        
        """
        event must have a int time field
        event must have a mess must implement send()
        """
        
        self.sequence.insert(self._real_to_tick(time),event)
      
        
          
    def start(self):
        """
        start the engine which should call play_events_at(at)
        """
        self.engine.start()
                  
    def _play_events_at(self,at):
        
        """
        Play messages and advance the time.
        """
        print at
        
        # if next event is after at just return
        if self.prev.next.time > at:
            return
        
        # catch up by skipping missed events
        while self.prev.next.time < at:
            self.prev=self.prev.next
        
        while self.prev.next.time  == at:
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
        
