import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt


key=['r-','b-']

class Plotter:
    
    def __init__(self,xlim,ylim,ylim2):
        plt.ion()
        self.fig = plt.figure()
        self.host = host_subplot(111, axes_class=AA.Axes)
        self.par1 = self.host.twinx()
        
        #self.ax = self.fig.add_subplot(111)
        self.lines=[None,None]
    
        self.host.set_xlim(xlim)
        self.host.set_ylim(ylim)
        self.par1.set_ylim(ylim2)
        
   
    
    def drawX(self,iline,x,y):
        
        if self.lines[iline] == None:
            if iline == 0:
                self.lines[iline], = self.host.plot(x, y, key[iline]) # Returns a tuple of line objects, thus the comma
            else:
                self.lines[iline], = self.par1.plot(x, y, key[iline]) # Returns a tuple of line objects, thus the comma
        else:        
            self.lines[iline].set_data(x,y)
        
    def redraw(self,title):
        plt.title(title) 
        self.fig.canvas.draw()
        
        
if __name__ == "__main__":
    x=np.linspace(0, 6*np.pi, 100)
    p=Plotter(x)
    
    
    n=len(x)
    y = np.sin(x)

# You probably won't need this if you're embedding things in a tkinter plot...
    
    win=np.ones(20)*(1.0/20.0)
 
    cnt=0
    for phase in np.linspace(0, 10*np.pi, 500):
        y=np.sin(x + phase)
        z=np.correlate(y, y, mode="full") 
        w=np.convolve(z, win, mode="same")   
        p.draw(w[n-1:],str(cnt))
        cnt+=1
    
