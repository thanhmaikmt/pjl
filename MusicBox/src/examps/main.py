import MB


import time
import beatclient
import sys

  
context=MB.Context()

melody_player=context.create_player(0)
echo_player=context.create_player(2)


class PhrasePlayerFirer:
    

    def __init__(self,player):
        self.player=player
        
    def notify(self,phraser):
        
        seq=context.get_sequencer()
        tNow=seq.get_stamp()
        self.phrase=phraser.phrases[-1]
        tHead=self.phrase.head.time
        tDelay=tNow-tHead
        self.pPlayer=MB.PhrasePlayer(self.phrase,seq,self.player)
        self.pPlayer.start(tDelay)
      
      
client=PhrasePlayerFirer(echo_player)

              
phraser=MB.Phrasifier(melody_player.list,melody_player.parser,1.0,client)

context.callback(phraser.visit,0,0.2)


map={"melody":melody_player.play}

context.start(map)
        
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
       
        beatlen=context.get_beatlength()
        str1="{:5.1f}".format(60.0/beatlen)
        self.bpm_val.SetLabel(str1)
        barlen=context.get_barlength()
        str1="{:5.1f}".format(4*60.0/barlen)
        self.bpm2_val.SetLabel(str1)
 
  #      self.but.after(1000,self.monit)  
    
    def make_panels(self):
        
    
        box = wx.BoxSizer(wx.VERTICAL)
    
        quit=wx.Button(self, 1, 'Quit')    
        box.Add(quit,1,wx.EXPAND)   
        quit.Bind(wx.EVT_BUTTON, self.OnClose)
         
        self.bpm=wx.StaticText(self,-1,"Beats Per Min")
        self.bpm_val=wx.StaticText(self,-1,"???")
        
        self.bpm2=wx.StaticText(self,-1,"Bars Per Min * 4")
        self.bpm2_val=wx.StaticText(self,-1,"???")
        midi_out=wx.StaticText(self,-1,"MidiOut:"+context.midi_out_dev.name)
      
        h1=wx.BoxSizer(wx.HORIZONTAL)
        v1 = wx.BoxSizer(wx.VERTICAL)
        v1.Add(self.bpm2, 1, wx.EXPAND)
        v1.Add(self.bpm, 1, wx.EXPAND)
        v1.Add(midi_out, 1, wx.EXPAND)
        h1.Add(v1,1)
         
        v2 = wx.BoxSizer(wx.VERTICAL)
        v2.Add(self.bpm2_val, 1, wx.EXPAND)
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
        pid.terminate()
        self.err_t = None
        context.quit()
       
        # wait for the pipes to flush
        time.sleep(.2)
        self.Destroy()
        print "OnClose End"
     

import subprocess
pid=subprocess.Popen([MB.PYTHON_CMD, "../FrontEnds/pg_ui.py"])
#pid=subprocess.Popen(["ls", "../FrontEnds"])


app = wx.PySimpleApp()
mainFrame = MyFrame(None, title='PYO-GA', pos=(50,50), size=(800,300))
mainFrame.Show()
app.MainLoop()

print " EXIT?"
  

