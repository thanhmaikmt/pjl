""" pygame MUSIC box front end 
    start the server before running
    Note the example tonality player starts this automaticlly
"""

import sys
sys.path.append('../MB')

import pgdriver
from pygame import * 
import OSC
import MBsetup



but_melody=[K_q,K_w,K_e,K_r,K_t,K_y,K_u,K_i,K_o,K_p,K_LEFTBRACKET,K_RIGHTBRACKET]

but_tonality=[K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9,K_0,K_MINUS,K_EQUALS]

but_cntrl=[K_SPACE,K_RETURN]


xmax=512
ymax=512

def but_pos(key,list):
    if key in list:
        return list.index(key)
    else:
        return -1
    
class Client:
    
    
    def __init__(self):
        addr=MBsetup.get_osc_ip()
        print "using ip", addr
        self.osc_client=OSC.OSCClient()
        self.osc_client.connect(addr)
        
        buts={}
        
        pos=0
        for k in but_melody:
            buts[k]="/1/melody/"+str(pos)
            pos+=1
        
        pos=0
        for k in but_tonality:
            buts[k]="/1/tonality/"+str(pos)
            pos+=1
            
        buts[K_SPACE]="/1/control/space"
    
        self.map=buts
        
    def handle(self,event):
        if event.type == KEYUP or event.type== KEYDOWN:
            key=event.key
            cmd=self.map.get(key,None)
            if cmd == None:
                return
            
            if event.type == KEYUP:                
                msg=OSC.OSCMessage(cmd,[0.0])
            else:
                msg=OSC.OSCMessage(cmd,[1.0])
                
            self.osc_client.send(msg)
            
        elif event.type == MOUSEMOTION:
            x= (event.pos[0]*127)/xmax
            y= (event.pos[1]*127)/ymax
            
            if x <=0 or x> 127 or y<=0 or y>127:
                return
#        if event.buttons[0]:
            cmd="/1/xy/"
            msg=OSC.OSCMessage(cmd,(x,y))
            self.osc_client.send(msg)
            
        

       
pe=pgdriver.PGDriver((Client()),(xmax,ymax)) 
pe.run()
pe.stop()
       