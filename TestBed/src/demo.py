'''
Created on 14 Dec 2010

@author: pjl
'''

import sys
#import DBStuff

import matplotlib 
matplotlib.use('GTK') 
from matplotlib.figure import Figure 
from matplotlib.axes import Subplot 
from matplotlib.backends.backend_gtk import FigureCanvasGTK, NavigationToolbar 
from numpy import arange, sin, pi 

class appGui: 
    def __init__(self): 
        gladefile = "project2.glade" 
        self.windowname = "gtkbench" 
        self.wTree = gtk.glade.XML(gladefile, self.windowname) 
        dic = {"on_window1_destroy" : gtk.main_quit, 
            "on_button1_clicked" : self.submitDB, 
            "on_button3_clicked" : self.fillTree, 
            "on_notebook1_switch_page" : self.selectNotebookPage, 
            "on_treeview1_button_press_event" : self.clickTree, 
            "on_button2_clicked" : self.createProjectGraph 
            }
        self.wTree.signal_autoconnect(dic)

  
try: 
    import pygtk 
    pygtk.require("2.0") 
except: 
    pass 
try: 
    import gtk 
    import gtk.glade 
except: 
    sys.exit(1)
