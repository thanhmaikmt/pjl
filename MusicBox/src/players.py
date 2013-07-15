import MBmusic
import array
import dlinkedlist



class Phrase:
    
    def __init__(self,head,tail):
        self.head=head
        self.tail=tail
        
        
 
class Phrasifier:
    
    def __init__(self,list,parser,tbreak,client):
        self.list=list
        self.notesOn=NotesOn(parser)
        self.phrases=[]
        self.ptr=self.list.head
        #  pointer to the first event in the current phrase.
        self.phrase_start=None 
        self.parser=parser
        self.tbreak=tbreak
        self.client=client
        
        
    def visit_next_event(self):
        nxt=self.ptr.next
        if  nxt == None:
            return False
        
        pitch,vel=self.parser.parse(nxt.data[0],nxt.data[1])
        
        onPrev=self.notesOn.isPlaying()
        
        self.notesOn.process(pitch,vel)

        onNow=self.notesOn.isPlaying()
        
        if self.phrase_start == None:  
            assert vel > 0
            assert not onPrev
            assert onNow
            self.phrase_start=nxt 
        elif not onPrev and onNow:
            if (nxt.time-self.ptr.time)> self.tbreak:
                self.phrases.append(Phrase(self.phrase_start,self.ptr))
                self.phrase_start=nxt
                self.client.notify(self)
                
        self.ptr=nxt
        
                
    def visit(self,tNow):
    
        """ process pending events
        """
        while self.ptr.next !=None:
            if  self.ptr.next.time > tNow:
                return
            self.visit_next_event()
           
        """ playing then obviously  not a phrase
        """ 
        if self.notesOn.isPlaying():
            return
        
        """ No phrase start
        """
        if self.phrase_start == None:
            return
        
        
        if tNow-self.ptr.time > self.tbreak:
            self.phrases.append(Phrase(self.phrase_start,self.ptr))
            self.phrase_start=None
            print "phrased"
            self.client.notify(self)
  

class BasicParser:
    
    def parse(self,toks,data):
        val=float(data[0])          
        pitch=int(toks[0])+48

        vel=int(val*127)
        return pitch,vel
    
      
#            
#         if self.score:
#                 beat=self.seq.get_stamp()
#                 pitch=self.score.get_tonality(beat).get_note_of_scale(i,self.score.key)+36
#         else:
#                 pitch=i+48    
#     
    
class NotesOn:
    
    def __init__(self,parser):#            
#         if self.score:
#                 beat=self.seq.get_stamp()
#                 pitch=self.score.get_tonality(beat).get_note_of_scale(i,self.score.key)+36
#         else:
#                 pitch=i+48    
#     
            self.notesOn={}
       
    def play_toks(self,toks,data):
        
        pitch,vel=self.parser.parse(toks,data)
        self.process(pitch,vel)
         
    def process(self,pitch,vel):
            if vel != 0:
                assert not self.notesOn.get(pitch)
                self.notesOn[pitch]=vel
            else:
                assert self.notesOn.get(pitch)
                del self.notesOn[pitch]
                
    def isPlaying(self):
        return len(self.notesOn)
    
    
class Player:
    
        """
        plays a melody instrument using the OSC  message
        """
    
        def __init__(self,inst,parser=None,seq=None,memory=True,beat_client=None):

            self.parser=parser
            
            if parser == None:
                self.parser=BasicParser()
                
            self.inst=inst
            self.seq=seq
            self.messenger=MBmusic.Messenger(inst)
            if memory:
                self.list=dlinkedlist.OrderedDLinkedList()
        # put a dummy head to avoid special cases.
                self.list.append(0.0,None)
            else:     
                self.list=None

                
            self.beat_client=beat_client
            
            
            
        def play(self,toks,data):
                 
            """
            Interpret the OSC message and play it
            """
             
            if toks[0] == 'xy':
                x=int(float(data[1])*127)
                y=int(float(data[0])*127)
                #print " melody xy",x,y
                self.messenger.inst.set_cc(12,x)
                self.meesenger.inst.set_cc(13,y)
                
                return
            
            
            pitch,vel=self.parser.parse(toks,data)
            
            
            #print "play",pitch,vel
  
            if vel != 0:
                self.messenger.inst.note_on(pitch,vel)
            else:
                self.messenger.inst.note_off(pitch)
        
            stamp=self.seq.get_real_stamp()
         
            if self.list != None:
                self.list.append(stamp,(toks,data))
                
            
     
            # beat=band.seq.get_beat()
            # print "STOMP",self.stamp
            if self.beat_client:
                self.beat_client.stomp(stamp)
        
        def set_instrument(self,name):
            pass
            
  
        def quit(self):
            if self.beat_client:
                self.beatclient.quit()

            
                
class PlayerWithMemory:
    
    def __init__(self,player,seq,client):
        self.list=dlinkedlist.OrderedDLinkedList()
        # put a dummy head to avoid special cases.
        self.list.append(0.0,None)     
        self.player=player
        self.client=client
        self.seq=seq
        self.stamp=seq.get_real_stamp()
        
    def play(self,toks,data):
        self.player.play(toks,data)
        self.stamp=self.seq.get_real_stamp()
        self.list.append(self.stamp,(toks,data))
       

        if not self.client:
            return
        
       # beat=band.seq.get_beat()
       # print "STOMP",self.stamp
        self.client.stomp(self.stamp)
        #print beat,toks,data
        #sys.exit()
        
        
        
        
    def quit(self):
        if self.client:
            self.beatclient.quit()
            
                            
class ChordPlayer:
        
        def __init__(self,inst,score,seq):
            self.pitches=[]
            self.template=[0,2,4,6]
            self.inst=inst
            self.score=score
            self.seq=seq
            
        def play(self,toks,data):
#           print "chord",toks,data
            
            if toks == "xy":
                y=int(float(data[0])*127)
                x=int(float(data[1])*127)
                self.inst.set_volume(y)
                return
            

            for pitch in self.pitches:
                self.inst.note_off(pitch)
                
            self.pitches=[]
                                        
           # inversion=int(toks[1])     #   TODO
            
            vel=int(float(data[0])*127)
            if vel == 0:
                return
            
            beat=self.seq.get_beat()
            tonality=self.score.get_tonality(beat)
            
            
            for p in range(len(self.template)):
                pit=tonality.get_note_of_chord(self.template[p],self.score.key)+48
                self.inst.note_on(pit,vel)
                self.pitches.append(pit)

        #  Play notes (shift up +12 if pitch is too low)     
#            for p in self.pitches:
#                while p < self.lowest:
#                    p += 12
#                

            
class MelodyPlayer:
    
        """
        plays a melody instrument using the OSC  message
        """
    
        def __init__(self,inst,score=None,seq=None):

            self.score=score
            self.inst=inst
            self.seq=seq
            self.player=MBmusic.Messenger(inst)
        
        def play(self,toks,data):     
            if toks[0] == 'xy':
                x=int(float(data[1])*127)
                y=int(float(data[0])*127)
                print " melody xy",x,y
                self.player.inst.set_cc(12,x)
                self.player.inst.set_cc(13,y)
                
                return
            
            val=float(data[0])
            
#            assert len(toks) >1
             
            i=int(toks[0])
            
            #print "Melody ",val,i
            vel=int(val*127)       
           
            
            if self.score:
                beat=self.seq.get_stamp()
                pitch=self.score.get_tonality(beat).get_note_of_scale(i,self.score.key)+36
            else:
                pitch=i+48    
            
            #print "play",pitch,vel
            
            if vel != 0:
                self.player.inst.note_on(pitch,vel)
            else:
                self.player.inst.note_off(pitch)
                # schedule the note off
                #playable = MBmusic.Playable(MBmusic.NoteOff(pitch), self.player)
                #self.seq.schedule(beat+0.05, playable)
    
    
    
  

class DelayedPlayer:
    
    """

      sched()
      fire()
    
    """
    
    def __init__(self,list,seq,player,delay,poll_dt):
        self.list=list
        self.seq=seq
        self.player=player
        self.delay=delay
        self.poll_dt=poll_dt
        assert poll_dt < delay
        
    def start(self):
        
        self.last=None
        self.tNow=self.seq.get_stamp()
        self.time1=self.tNow+self.delay
        self.grazer=dlinkedlist.DLinkedListGrazer(self.list)
        
        #  hack to avoid special case of an empty list.
        # listmust contian an event in the past so we can have a self.last
        assert self.list.head != None
        assert self.list.head.time < self.time1
        
        self.last=self.list.head
        while self.last.next != None  and self.last.next.time <self.time1:
            self.last=self.last.next
        
        self.sched()
        
    def sched(self):
        """
        schedule to fire at next event in list OR after self.delay
        """
        
        # schedule a fire at next event or after a delay if none
        
        tSched=self.tNow+self.poll_dt
        
        if self.last != None and self.last.next != None:             
            tNext=self.last.next.time+self.delay
            assert tNext > self.seq.get_stamp()
            tSched=min(tSched,tNext)
        
            
        self.seq.schedule(tSched,self)
            
         
    def fire(self,tt):
        
        
        """ 
        tt is the time according to the sequencer
        """
        
        self.tNow=self.seq.get_stamp()
        
        # play all events between time1 and time2
        time2=self.seq.get_stamp()-self.delay
        self.grazer.set_range(self.time1,time2)
        
        while True:
            node=self.grazer.next()
            if node and node.data:
                toks=node.data[0]
                data=node.data[1]
                # print "---- PLAY ",self.tNow,toks,data
                self.player.play(toks,data) 
                self.last=node                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
            else:
                break   

        self.time1=time2
        self.sched()
        
        

class PhrasePlayer:
    
    """
      sched()
      fire()
    """
    
    def __init__(self,phrase,seq,player):
        self.phrase=phrase
        self.seq=seq
        self.player=player
        
        
    def start(self,t_shift,tloop=None):
        """
        start playing the phrase shifted by t_shift
        that is as if the timeplay=event.time+t_shift  
        """
        
        if tloop:
            assert tloop >= self.phrase.tail.time-self.phrase.head.time
            
        tNow=self.seq.get_stamp()
        self.t_shift=t_shift
        self.ptr=self.phrase.head
        tNext=self.ptr.time+t_shift
        self.tloop=tloop
        if tNext<tNow:
            print "ooops PhrasePlayer:start: too late"
        
        self.sched()
        
    def sched(self):
   
        
        """
        schedule to fire at next event in list OR after self.delay
        """
        
        tEvent=self.ptr.time+self.t_shift    
             
        self.seq.schedule(tEvent,self)
            
         
    def fire(self,tt):
        
        
        """ 
        tt is the time according to the sequencer
        """
        
        self.tNow=self.seq.get_stamp()
        
        
        while True:
                toks=self.ptr.data[0]
                data=self.ptr.data[1]
                # print "---- PLAY ",self.tNow,toks,data
                self.player.play(toks,data) 
                if self.ptr == self.phrase.tail:
                    if self.tloop:
                        self.t_shift=self.t_shift+self.tloop
                        self.ptr=self.phrase.head
                        break
                    return
                
                self.ptr=self.ptr.next
                if self.ptr.time+self.t_shift > tt:
                    break
                
        self.sched()
                
 
   