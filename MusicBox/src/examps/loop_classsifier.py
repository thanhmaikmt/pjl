
import MB

import dlinkedlist
import players
import time

class A:
    
    def __init__(self,player):
        self.list=dlinkedlist.OrderedDLinkedList()
        self.player=player
        
    def melody(self,toks,data):
        self.player.play(toks,data)
        vel=float(data[0])
        if vel==0.0:
            return
        beat=band.seq.beat
        tt=time.time()
        self.list.append(tt,toks)
        print beat,toks,data




band=MB.Band()

score=None

melody_player=players.MelodyPlayer(band.solo_inst,None,band.seq)

a=A(melody_player)

map={"melody":a.melody}
band.start()


addr=MB.get_osc_ip()
osc_driver=MB.Server(addr,map,None)
osc_driver.run()

import os
#os.system("/usr/local/bin/python ../FrontEnds/midi_ui.py")
os.system("/usr/local/bin/python ../FrontEnds/pg_ui.py")
   
xx=raw_input("HIT CR")

band.quit()
osc_driver.quit()