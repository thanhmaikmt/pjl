
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
        self.player=player
        self.client=client
        self.seq=seq
        
    def melody(self,toks,data):
        self.player.play(toks,data)
        tt=self.seq.get_stamp()
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
        
        self.tNow=self.seq.get_stamp()
        self.time1=self.tNow+self.delay
        self.grazer=dlinkedlist.DLinkedListGrazer(self.list)
        self.sched()
        
    def sched(self):
        """
        schedule to fire at next event in list OR after self.delay
        """
        node=self.grazer.seek(self.time1)
        # schedule a fire at next event or after a delay if none
            
        if node == None or node.next == None :             
            #  No events in queue 
            #  revisit after a delay
            print " FREERUN SCHED AT ",self.tNow+self.poll_dt
            self.seq.schedule(self.tNow+self.poll_dt,self)
        else:
            print " EVENTSCHED AT ",node.next.time+self.delay
            self.seq.schedule(node.next.time+self.delay,self)
            
            
         
    def fire(self,tt):
        """ 
        tt is the time according to the sequencer
        """
        
        self.tNow=self.seq.get_stamp()
        
        # we need to seek because a time will have elapsed since we scheduled this fire
        # if the list has changed we need to make sure we play new events
        node=self.grazer.seek(self.time1)
     
        # play all events between time1 and time2
        time2=tt-self.delay
        
        if node != None:
            while True:
                node=self.grazer.advance(time2)
                if node:
                    toks=node.data[0]
                    data=node.data[1]
                    self.player.play(toks,data)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                else:
                    break   
                
        self.time1=time2
        self.sched()
            



band=MB.Band()
                                                                                                                                                                                                                                                                                                                                                                                                                        
score=None

melody_player=players.MelodyPlayer(band.solo_inst,None,band.seq)

beatclient=None   #beatclient.Client(debug=False)
a=A(melody_player,band.seq,beatclient)
b=DelayedPlayer(a.list,band.seq,melody_player,2.0,0.5)
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