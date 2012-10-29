import wx


  
if __name__ == "__main__":
     
    app = wx.PySimpleApp()
    mainFrame = MyFrame(None, title='PYO-GA', pos=(50,50), size=(800,300))
    mainFrame.Show()
    app.MainLoop()