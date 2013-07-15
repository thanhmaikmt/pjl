import wx


            


import  string
import  wx


#---------------------------------------------------------------------------

class MyTreeCtrl(wx.TreeCtrl):
    def __init__(self, parent, id, pos, size, style):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)


    def OnCompareItems(self, item1, item2):
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        self.log.WriteText('compare: ' + t1 + ' <> ' + t2 + '\n')
        if t1 < t2: return -1
        if t1 == t2: return 0
        return 1

#---------------------------------------------------------------------------

class TestTreeCtrlPanel(wx.Panel):
    def __init__(self, parent):
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
        #self.Bind(wx.EVT_SIZE, self.OnSize)


        tID = wx.NewId()

        self.tree = MyTreeCtrl(self, tID, wx.DefaultPosition, (500,300),
                               wx.TR_HAS_BUTTONS
                               | wx.TR_EDIT_LABELS
                               #| wx.TR_MULTIPLE
                               #| wx.TR_HIDE_ROOT
                               )
        self.root = self.tree.AddRoot("The Root Item")
        
        
        fil=open("CP300.txt","r")
        
        while True:
            line=fil.readline()
            print line
            if line[0:6] == '[mode]':
                break
        
        nodes=[self.root,None,None,None]
        for l in fil:
            print l
            if l[0]=='[':
                toks=l.split(']')
                str1=toks[0][1:]
                str2=toks[1][:-1]
                if str1[0] == 'g' or str1[0]=='p':
                    level=int(str1[1])
              
                    nodes[level] = self.tree.AppendItem(nodes[level-1], str2)
            
                    
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
         
         
    def OnSelChanged(self, event):
        self.item = event.GetItem()
        if self.item:
            print "OnSelChanged: %s\n" % self.tree.GetItemText(self.item)
        
        event.Skip()
        

class MyFrame(wx.Frame):
 
        
    def __init__(self,parent, title, pos, size=(300, 250)):
        wx.Frame.__init__(self, parent, -1, title, pos, size)
        
        tree=TestTreeCtrlPanel(self)
        self.Layout()
        
        
        
        
app = wx.PySimpleApp()
mainFrame = MyFrame(None, title='Patch', pos=(50,50), size=(800,300))
mainFrame.Show()
app.MainLoop()
