import linkedlist
import sys
import time
from threading import Thread
from  setup import *

SLEEP_TIME=0.001    # tick to yield in engine event loop

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
            
            
    def stop(self):
        
        print  "Engine stopping"
        if not self.running:     # make sure we don't do this twice
            return
        
        self.running=False      # flag deamon to halt.
        self.join()            
        
         
class Playable:
    
    """
    A Playable is a message and a player
    The player must be able to send the message of the event
    """
    def __init__(self,mess,player):
        self.mess=mess
        self.player=player
        
    def fire(self):
        self.player.play(self.mess)


 
class Phrase:
    """
    Is a list of Messages with times
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
        self.sequence.insert(-sys.maxint,None)
        self.sequence.insert(sys.maxint,None)
        
        self.engine=Engine(bpm,ticks_per_beat,self._play_events_at)

        self.beat=0
        self.ticks_per_beat=ticks_per_beat
        
        # self.prev is last event to be played
        self.prev=self.sequence.head

        
        # next should be OK providing we have an end event in the sequence

    def _beat_to_tick(self,beat):
        return int(beat*self.ticks_per_beat)
   
   
    def schedule_at(self,start,phrase,player):    
        for node in phrase:
            self.add(node.tick+start,Playable(node.data,player))
            
   
    def add(self,time,event,prio=0):
        
        """
        event must have a int tick field
        event must have a mess must implement send()
        """
        
        self.sequence.insert(self._beat_to_tick(time)-prio,event)
      
    def add_after(self,delay,event,prio=0):
        
        """
        event must have a int tick field
        event must have a mess must implement send()
        """
        
        self.sequence.insert(self._beat_to_tick(self.beat+delay)-prio,event)
        
          
    def start(self):
        """
        start the engine which should call play_events_at(at)
        """
        self.engine.start()
      
    def quit(self):
        self.engine.stop()
        
                    
    def _play_events_at(self,at):
        
        """
        Play messages and advance the tick.
        """
        
        self.beat=float(at)/self.ticks_per_beat
         
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
#        print (mess)   
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
        
        
    
class Groove:
    
    """
    Parameters: delats= a list of times (delta times).
                player  a player that is called for each time(with a count)
    
    To repeat a Groove use a Repeater.
    
    """
     
    def __init__(self,seq,**kwargs):
        self.times=kwargs['deltas']
        
        self.iter=self.times.__iter__()
        
        seq.add_after(self.iter.next(),self)
        
        self.seq=seq
        self.count=0
        self.n=len(self.times)
        self.player=kwargs['player']
        
        
    def fire(self):
        
        #print self.count," Groove fire",seq.beat
        
        self.player.play_count(self.count)
        self.count+=1
        if self.count >= self.n:
            return
                    
        self.seq.add_after(self.iter.next(),self)          

        
        
class Repeater:
    """
    Creates instances of a client every period from start.
    **kwargs are passed to the Client
    """
    
    def __init__(self,start,period,seq,Client,**kwargs):
        self.start=start
        self.period=period
        self.Client=Client
        seq.add(start,self)
        self.kwargs=kwargs
        self.seq=seq
        
        
    def fire(self):
        if DEBUGGING:
            print " Send " ,self.kwargs
            
        self.Client(self.seq,**self.kwargs)
        
        self.seq.add_after(self.period,self)
         #TODO delete etc.....
 
