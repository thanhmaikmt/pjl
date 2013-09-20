import linkedlist
import sys
import time
from threading import Thread
import MBsetup as MB

CSI="\x1B["
RED='\033[91m'
ENDC = '\033[0m'

SLEEP_TIME=0.001    # tick to yield in engine event loop

class Engine(Thread):


    """Engine calls a call_back every tick (dt)
       The Engine will attempt to keep the tick synchrounized with
       real time using  a sleep (which will yield. to allow multithreading)
       For usage see Sequencer.
    """


    def __init__(self,dt,call_back=None):
        
        self.dt=dt
        self.call_back=call_back
        self.tclock=0.0
        Thread.__init__(self)
        self.running=False
        
        
    
    
    def run(self):
        self.run2()
        
    def run1(self):
        self.running=True
        
        tnext=tnow=time.time()
        
        while self.running:
            
            # spin until next tick
            
            while tnow < tnext:
                # yeild to other threads
                time.sleep(SLEEP_TIME) 
                tnow=time.time()       
            
            self.call_back()
            
            
            self.tclock+=self.dt
            tnext+=self.dt
    
    
    def run2(self):
        self.running=True
        
        
        self.call_back()
            
        tnow=time.time()
        tnext=tnow+self.dt
        
        while self.running:
            tnow=time.time()
            sleep_time=tnext-tnow
            
            if sleep_time>0:
            # spin until next tick
            # yeild to other threads
                time.sleep(sleep_time)
            else:
                print '>',
                   
            self.call_back()
            tnext+=self.dt
            
            
    def stop(self):
        
        print  "Engine stopping"
        if not self.running:     # make sure we don't do this twice
            return
        
        self.running=False      # flag deamon to halt.
        self.join()            
        print  "Engine stopped (threads joined)"




class Sequencer(Engine):
    
    """
    Plays a sequence of messages
    Delegates the timing to an engine which
    must call play_events_at(at) with at incrementing each call
    
    stamp is real time
    """
    
    def __init__(self,dt=0.005):
        """
        Create a Sequencer that services events at a rate of dt
        """     
        self.sequence=linkedlist.OrderedLinkedList()        
        self.sequence.insert(-sys.float_info.max,None,None)
        self.sequence.insert(sys.float_info.max,None,None)
        
        Engine.__init__(self,dt,self._play_next_dt)
        
        # self.prev is last event to be played
        self.prev=self.sequence.head
        self.time=0.0
        self.tstart=time.time()
     
    def schedule(self,at,event):
        """
        add an event to the queue at time = at
        
        """
        
        # time=self.beat_to_time(beat)  
        if at+self.dt < self.time:
            print RED+"Schedule underrun "+ENDC,at,self.time
            
        self.sequence.insert(at,event,self.prev)
      
          
    def quit(self):
        """
        Stop the engines. 
        """
        
        self.stop()
        
                    
    def _play_next_dt(self):
        
        """
        advance self.time by self.dt 
        play any pending events up to and including   
        self.time
        """
        
        #print "SEEQ PLAY NEXT"

        self.time+=self.dt
        # if next event is after at just return
        if self.prev.next.time > self.time:
            return
        
        # play pending events   
        while self.prev.next.time <= self.time:
            self.prev=self.prev.next
            # pass the unquantized version of the time to the player.
            # this would allow higher resolution playback if we could be bothered.
            self.prev.data.fire(self.prev.time)
            
    def get_real_stamp(self):
        """
        Get the time using the clock
        """
        return time.time()-self.tstart

    def get_stamp(self):
        """
        Get the stamp according to the schedulers last schedule
        """
        return self.time

class SequencerBPM(Engine):
    
    """
    Plays a sequence of messages
    Delegates the timing to an engine which
    must call play_events_at(at) with at incrementing each call
    
    stamp is the beat 
    """
    
    def __init__(self,beats_per_sec=1.0,dt=0.005):
                
        self.sequence=linkedlist.OrderedLinkedList()        
        self.sequence.insert(-sys.float_info.max,None,None)
        self.sequence.insert(sys.float_info.max,None,None)
        
        Engine.__init__(self,dt,self._play_next_dt)
        
        # self.prev is last event to be played
        self.prev=self.sequence.head
        self.beats_per_sec=beats_per_sec        
        self.beat=0.0
        self.time=0.0
     
     
    def schedule(self,beat,event):
        # time=self.beat_to_time(beat)  
        self.sequence.insert(beat,event,self.prev)


#        
#    def beat_to_time(self,beat):
#        
#        #  how many beats from the last count
#        ttt=beat-self.beat    
#        
#        tt_time=self.tclock+self.beats_per_sec*ttt
#        return tt_time
#  
      
      
      
    def quit(self):
        """
        Stop the engines. 
        """
        
        self.stop()
        
                    
    def _play_next_dt(self):
        
        """
        advanve beat by dt and 
        play any pending events
        """
        
        #print "SEEQ PLAY NEXT"
        self.time+=self.dt
        self.beat+=self.beats_per_sec*self.dt
        # if next event is after at just return
        if self.prev.next.time > self.beat:
            return
        
        # play pending events   
        while self.prev.next.time <= self.beat:
            self.prev=self.prev.next
            self.prev.data.fire(self.prev.time)

    def get_stamp(self):
        return self.beat
     
     
    def get_real_stamp(self):
        """
        Get the time using the clock (TODO MAKE THIS ACCURATE).
        """
        return self.beat
    
    def set_bpm(self,bpm):
            self.beats_per_sec=bpm/60.0
    
 
class Playable:
    
    """
    A Playable is a message and a player
    The player must be able to send the message of the event
    """
    def __init__(self,mess,player):
        self.mess=mess
        self.player=player
        
    def fire(self,beat):
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

        
class Messenger:
        
    """
    Has an instrument and ....
    """
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
        
        
    
class Groover:
    """ Calls player.play_count(count,data)
        the data.deltas are used to time the calls.
        
        count is incremented each call.
    """

    def __init__(self,start,seq,data,player):
        
        """
        start --  time of groove start (may not be first event)
        seq --    sequencer
        data --   info passed to player
        player -- plays the event using play_count(count,data)
        """ 
        
        self.times=data.times 
        self.data=data       
        self.seq=seq
        self.beat_ref=start
        self.iter=self.times.__iter__()
        self._schedule()
       
        self.count=0
        self.n=len(self.times)
        self.player=player
        
    def _schedule(self):
        beat=self.iter.next()+self.beat_ref
        self.seq.schedule(beat,self)
         
        
    def fire(self,beat):
        
        #print self.count," Groove fire",seq.beat
        
        self.player.play_count(self.count,self.data,beat)
        self.count+=1
        if self.count >= self.n:
            return
             
        self._schedule()       
        
        
        #self.seq.add_after(self.iter.next(),self)          
    
    


class GrooverFactory:
    
    """  Creates Groovers 
    Parameters: deltas= a list of times (delta times).
                player  a player that is called for each time(with a count)
    
    """
     
    def __init__(self,seq,data,player):
        self.data=data       
        self.player=player
        self.seq=seq
        
    def create(self,when):
        return Groover(when,self.seq,self.data,self.player)
        
        

        
        
class Repeater:
    """  Calls the given func periodically
    """
    
    def __init__(self,start,period,seq,func):
        
        """
        start -- time of first call to func
        period -- interval between calls
        func --- function to be called with beat as an argument
        """
        
        self.start=start
        self.period=period
        self.func=func
        seq.schedule(start,self)
        self.seq=seq
            
    def fire(self,beat):
        self.func(beat)
        self.seq.schedule(beat+self.period,self)
        


     
     
class Score:
 
 
    def __init__(self, nbars,beats_per_bar,key):
        self.beats_per_bar = beats_per_bar 
        self.bars_per_section = nbars
        self.beats_per_section=nbars*beats_per_bar
        self.key=key
 
        self.tonalities = []

        for i in range(self.beats_per_section):
            self.tonalities.append(None)
  
        self.look_ahead=0.5  #  look ahead 1/2 a beat when reporting tonality
        
#        seq.schedule(start -priority, self)
#        self.seq = seq
# 
    def set_tonality(self,tonality,bar=0,beat=None):
        
        if beat != None:
            self.tonalities[bar*self.beats_per_bar+beat]=tonality
        else:
            for i in range(self.beats_per_bar):
                self.tonalities[bar*self.beats_per_bar+i]=tonality
                
    def get_tonality(self,beat):
        beati = int(beat+self.look_ahead)
        return self.tonalities[beati % self.beats_per_section]
    
#    
#    def fire(self,beat):
#        # print "Score fire "
#        self.seq.schedule(self.beat, self)
##        if self.beat % self.beats_per_bar == 0: 
##            self.beat_one_time = self.beat
#        
#    def get_count(self):
#        return self.beat % self.beats_per_bar      
#    
#    def get_time(self):
#        return self.seq.beat
 
class Tonality:
    
    """ Tonality is a scale + chord pattern. It needs a key to be concrete
    scale is the set of notes to be used.
    root= reference note in the scale 
    chord is indices of note in scale that make up the chord off set by root.
    
    e.g.
    
    key+scale[i]                  plays to scale
    key+scale[root+chord[i]]      plays arpeggio 
    """
     
    def __init__(self, scale, chord, root):
        self.chord = chord
        self.root = root
        self.scale = scale
        
        
    def get_note_of_chord(self, i, key):
        
        assert i < len(self.chord)
        ii = self.root + self.chord[i]
        assert ii < len(self.scale)
        return key + self.scale[ii]
    
           
        
    def get_note_of_vamp(self, i, key):
        
        assert i < len(self.chord)
        ii = self.root + self.chord[i]
        assert ii < len(self.scale)
        return  48+key + self.scale[ii]
    
    
    def get_note_of_chordscale(self, i, key):
        """
        Same as get note of scale but offset so i=0 returns the root
        """
        
        ii = self.root + i
        assert ii < len(self.scale)
        return key + self.scale[ii]
    
    def get_note_of_scale(self, i, key):
        
        ii = i
        assert ii < len(self.scale)
        return key + self.scale[ii]

class Metro:
    """ Simple Metronome with an accent and weak beat.
    """
    debug=False
    
             
    def __init__(self,start_beat,beats_per_bar,seq,inst,note_accent,note_weak):
        seq.schedule(start_beat,self)
        
        
        self.seq=seq
        self.accent=note_accent
        self.weak=note_weak
        self.count=0
        self.beats_per_bar=beats_per_bar
        self.inst=inst
        self.tlast=0        
                
    
    def fire(self,beat):
        
        if self.debug:
            tnow=time.time()
            delta=tnow-self.tlast
            self.tlast=tnow
            print " Metro.fire",delta
    
        if self.count %self.beats_per_bar == 0:
            self.accent.send(self.inst)
        else:
            self.weak.send(self.inst)
        
        self.count+=1
        self.seq.schedule(self.count,self)
        #TODO delete etc.....

    def schedule(self,beat,firer):
        t=self.beat_to_time(beat)
        self.seq.schedule(t,firer)

class BassPlayer:
 
    """ plays chords based on the tonality returned by the score.
        play_count(count,data,anchor) is called to initiate each chord.
        the Chorder expects the data to have a dur and velocity members to set the length and velocity.
        A BassPlayer is used by a Groover.
        The Groover is responisible for call play_count at the start of each count event.
        The Playable is responsible for scheduling any  NoteOff events
    """
    
    def __init__(self, seq, inst, score, lowest,highest):
           
        self.seq = seq
        self.score = score        
        self.inst = inst
        self.lowest  = lowest
        self.highest = highest
        self.player  = Messenger(inst)
        
        
    def play_count(self, count, data, beat):
        """ Used to play a event associated with the given count
        count -- increments each call
        beat  --  time of the event
        data  --  data for playing 
        """
        
        # print " Vamp.fire"
        
        tonality = self.score.get_tonality(beat)
        
        dur = data.durs[count]
        velocity = data.vels[count]
     
        pitch=tonality.get_note_of_chordscale(data.pattern[count],self.score.key)
    
        #print pitch,self.score.key
    
        # TODO Voicings
        #  Play notes (shift up +12 if pitch is too low)     
        while pitch < self.lowest:
            pitch += 12
   
 
    
        while pitch > self.highest:
            pitch -= 12
        
        #print pitch
        # play the note on
        self.inst.note_on(pitch, velocity)
        
        # schedule the note off
        playable = Playable(NoteOff(pitch), self.player)
        
        
        self.seq.schedule(beat+dur, playable)

 
class ChordPlayer:
 
    """ plays chords based on the tonality returned by the score.
        play_count(count,data) is called to initiate each chord.
        the Chorder expects the data to have a dur and velocity members to set the length and velocity
    """
    def __init__(self, seq, inst, score, lowest,template):
        
        
        self.seq = seq
        self.score = score        
        self.inst = inst
        self.lowest = lowest
        self.player = Messenger(inst)
        self.template=template
        
    def play_count(self, count, data,beat):
        """ Used to play a event associated with the given count
        """
        
        # print " Vamp.fire"
        
        tonality = self.score.get_tonality(beat)
        
        dur = data.durs[count]
        velocity = data.vels[count]
            
        pitches = []
        for p in range(len(self.template)):
            pitches.append(tonality.get_note_of_chord(self.template[p],self.score.key))
    
    
        # TODO Voicings
        
        #  Play notes (shift up +12 if pitch is too low)     
        for p in pitches:
            while p < self.lowest:
                p += 12
            
            # play the note on
            self.inst.note_on(p, velocity)  
    
            # schedule the note off
            playable = Playable(NoteOff(p), self.player)
            self.seq.schedule(beat+dur, playable)



def extend_by(noct,scale):
    n=len(scale)
    for octi in range(noct):
        for i in range(n):
            scale.append(scale[i] + (octi + 1) * 12)

major_scale = [0, 2, 4, 5, 7, 9, 11]    


extend_by(11,major_scale) 

#print (major_scale)

stack3 = [0, 2, 4, 6, 8, 10 ,12 ]

C=0
D=2
E=4
F=5
G=7
A=9
B=11

I=Tonality(major_scale, stack3, 0)
ii=Tonality(major_scale, stack3, 1)
iii=Tonality(major_scale, stack3, 2)
IV=Tonality(major_scale, stack3, 3)
V=Tonality(major_scale, stack3, 4)
vi=Tonality(major_scale, stack3, 5)
viio=Tonality(major_scale, stack3, 6)

tonalities=[I,ii,iii,IV,V,vi,viio]