
import MB

import dlinkedlist
import players
import time
import beatclient


# class Timer:
#     
#     def __init__(self):
#         self.tref=time.time()
#         
#         
#     def time(self):
#         return time.time()-self.tref
        
class A:
    
    def __init__(self,player,seq,client):
        self.list=dlinkedlist.OrderedDLinkedList()
        # put a dummy head to avoid special cases.
        self.list.append(-100.0,None)
        
        self.player=player
        self.client=client
        self.seq=seq
        
    def melody(self,toks,data):
        self.player.play(toks,data)
        tt=self.seq.get_stamp()
        
        #print "Appending",tt,toks,data
        self.list.append(tt,(toks,data))
     
        vel=float(data[0])
        if vel==0.0:
            return
        
        if not self.client:
            return
        
       # beat=band.seq.get_beat()
        print "STOMP",tt
        self.client.stomp(tt)
        #print beat,toks,data
        
    def quit(self):
        if self.client:
            self.beatclient.quit()


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
            
#         elif self.last==None and self.list.head != None:
#             tNext=self.list.head.time+self.delay
#             if tNext> self.tNow:
#                 tSched=min(tSched,tNext)
#             
        #print " EVENTSCHED AT ",tSched
        
            
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
            if node:
                toks=node.data[0]
                data=node.data[1]
                # print "---- PLAY ",self.tNow,toks,data
                self.player.play(toks,data) 
                self.last=node                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
            else:
                break   

        self.time1=time2
        self.sched()
            



band=MB.Band()
                                                                                                                                                                                                                                                                                                                                                                                                                        
score=None

melody_player=players.MelodyPlayer(band.solo_inst,None,band.seq)

beatclient=None   #beatclient.Client(debug=False)
a=A(melody_player,band.seq,beatclient)
b=DelayedPlayer(a.list,band.seq,melody_player,2.0,1.0)
b.start()

map={"melody":a.melody}
band.start()


addr=MB.get_osc_ip()
osc_driver=MB.Server(addr,map,None)
osc_driver.run()
# 
# import os
# #os.system("/usr/local/bin/python ../FrontEnds/midi_ui.py")
# os.system("python ../FrontEnds/pg_ui.py")
#    
xx=raw_input("HIT CR")

band.quit()
osc_driver.quit()
a.quit()