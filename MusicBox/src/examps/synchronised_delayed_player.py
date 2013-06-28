import MB

import dlinkedlist
import players
import time
import beatclient
 
class User:
    
    def __init__(self,player,seq,client,tbreak=2.0):
        self.list=dlinkedlist.OrderedDLinkedList()
        # put a dummy head to avoid special cases.
        self.list.append(0.0,None)     
        self.player=player
        self.client=client
        self.seq=seq
        self.stamp=seq.get_real_stamp()
        self.phrases=[]
        #  pointer to the first event in the current phrase.
        #
        self.phrase_start=None 
        
    def melody(self,toks,data):
        playing=self.player.is_playing() 
        last_stamp=self.list.tail.stamp
        self.player.play(toks,data)
        self.stamp=self.seq.get_real_stamp()
     
        vel=float(data[0])
     
        # if we are not playing and the time since the last event is greater than self.tbreak
        #   mark section of list as a phrase.
        #   set start of next phrase to the event we are now playing        
        #   initial event is a special case delt with by testing phrase_start equal to None 
        if not playing and self.phrase_start and (self.stamp-last_stamp) < self.tbreak:
            self.phrases.append((self.phrase_start,self.list.tail))
 
            # if this is not a note on something has gone wrong!!!!!
            assert vel > 0
            
            #print "Appending",tt,toks,data
            self.list.append(self.stamp,(toks,data))
            self.phrase_start=self.list.tail
            
        else:
            self.list.append(self.stamp,(toks,data))
                
        # If we are starting off then the
        if not self.phrase_start:
            self.phrase_start=self.list.tail
                        
        

        
        if vel==0.0:
            return 
        
        if not self.client:
            return
        
       # beat=band.seq.get_beat()
       # print "STOMP",self.stamp
        self.client.stomp(self.stamp)
        #print beat,toks,data
        
        
    def check_for_phrases(self):
        ptr=phrase
        playing=self.player.is_playing() 
        last_stamp=self.list.tail.stamp
        stamp_now=self.seq.get_real_stamp()
     
        vel=float(data[0])
     
        # if we are not playing and the time since the last event is greater than self.tbreak
        #   mark section of list as a phrase.
        #   set start of next phrase to the event we are now playing        
        #   initial event is a special case delt with by testing phrase_start equal to None 
        if not playing and self.phrase_start and (self.stamp-last_stamp) < self.tbreak:
            self.phrases.append((self.phrase_start,self.list.tail))
 
            # if this is not a note on something has gone wrong!!!!!
            assert vel > 0
            
            #print "Appending",tt,toks,data
            self.list.append(self.stamp,(toks,data))
            self.phrase_start=self.list.tail
            
        else:
            self.list.append(self.stamp,(toks,data))
                
        # If we are starting off then the
        if not self.phrase_start:
            self.phrase_start=self.list.tail
                        
        
        
    def quit(self):
        if self.client:
            self.beatclient.quit()

    def get_inactive_time(self):
        if self.player.is_playing():
            return 0;
    
        return seq.get_real_stamp()-self.stamp
    

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
 
 
context=MB.init()
melody_player=MB.create_player(0)
cpu_player=MB.create_player(2)
seq=context.get_sequencer()

beat=beatclient.Client(debug=False)

user=User(melody_player,seq,beat)
cpu=DelayedPlayer(user.list,seq,cpu_player,2.0,1.0)
cpu.start()

map={"melody":user.melody}
MB.start(map)
        
import wx
  
class MyFrame(wx.Frame):
   
        
    def __init__(self,parent, title, pos, size=(300, 250)):
        wx.Frame.__init__(self, parent, -1, title, pos, size)

      #  self.Bind(wx.EVT_IDLE,self.monit)
        self.make_panels()
        self.timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
     
        print "TTT=",self.timer.Start(1000)
        
    def update(self,evt):
        str1=str(user.get_inactive_time())
        str2="{:5.1f}".format(beat.get_bpm())
        self.inactive_val.SetLabel(str1)
        self.bpm_val.SetLabel(str2)
        
  #      self.but.after(1000,self.monit)  
    
    def make_panels(self):
        
        
        
        
        box = wx.BoxSizer(wx.VERTICAL)
    
        quit=wx.Button(self, 1, 'Quit')    
        box.Add(quit,1,wx.EXPAND)   
        quit.Bind(wx.EVT_BUTTON, self.OnClose)
         
        self.bpm=wx.StaticText(self,-1,"BPM")
        self.inactive=wx.StaticText(self,-1,"Space")
        self.bpm_val=wx.StaticText(self,-1,"???")
        self.inactive_val=wx.StaticText(self,-1,"???")
      
        h1=wx.BoxSizer(wx.HORIZONTAL)
        v1 = wx.BoxSizer(wx.VERTICAL)
        v1.Add(self.inactive, 1, wx.EXPAND)
        v1.Add(self.bpm, 1, wx.EXPAND)
        h1.Add(v1,1)
         
        v2 = wx.BoxSizer(wx.VERTICAL)
        v2.Add(self.inactive_val, 1, wx.EXPAND)
        v2.Add(self.bpm_val, 1, wx.EXPAND)
        h1.Add(v2,1)
#         
        box.Add(h1, 1)
#         
        self.SetAutoLayout(True)
        self.SetSizer(box)

        self.Layout()
        
        
        
             
    def  make_button_panel(self,parent):
        
        
        panel=wx.Panel(parent,-1, style=wx.SUNKEN_BORDER)
        box = wx.BoxSizer(wx.HORIZONTAL)
        
      
        
        panel.SetSizer(box)
        return panel
        
        
   
    def OnClose(self,event):
        print "CLosing"
        self.err_t = None
        MB.quit()
       
        # wait for the pipes to flush
        time.sleep(.2)
        self.Destroy()
     

app = wx.PySimpleApp()
mainFrame = MyFrame(None, title='PYO-GA', pos=(50,50), size=(800,300))
mainFrame.Show()
app.MainLoop()

  

