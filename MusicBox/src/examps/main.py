import MB

import dlinkedlist

import time
import beatclient
import sys

  
context=MB.init()
melody_player=MB.create_player(0)


phraser=MB.Phrasifier(melody_player.list,melody_player.parser,1.5)

context.callback(phraser.visit,0,0.5)

map={"melody":melody_player.play}

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
        pass
     #   str1=str(user.phrasifier.get_inactive_time())
       # str2="{:5.1f}".format(beat.get_bpm())
       # self.inactive_val.SetLabel(str1)
      #  self.bpm_val.SetLabel(str2)
        
  #      self.but.after(1000,self.monit)  
    
    def make_panels(self):
        
    
        box = wx.BoxSizer(wx.VERTICAL)
    
        quit=wx.Button(self, 1, 'Quit')    
        box.Add(quit,1,wx.EXPAND)   
        quit.Bind(wx.EVT_BUTTON, self.OnClose)
         
        self.bpm=wx.StaticText(self,-1,"BPM")
        self.bpm_val=wx.StaticText(self,-1,"???")
        self.inactive=wx.StaticText(self,-1,"Space")
        self.inactive_val=wx.StaticText(self,-1,"???")
        midi_out=wx.StaticText(self,-1,"MidiOut:"+context.midi_out_dev.name)
      
        h1=wx.BoxSizer(wx.HORIZONTAL)
        v1 = wx.BoxSizer(wx.VERTICAL)
        v1.Add(self.inactive, 1, wx.EXPAND)
        v1.Add(self.bpm, 1, wx.EXPAND)
        v1.Add(midi_out, 1, wx.EXPAND)
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
        pid.terminate()
        self.err_t = None
        MB.quit()
       
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
  

