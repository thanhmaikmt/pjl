import matplotlib.pyplot as plt
import numpy as np



class Plotter:
    
    def __init__(self,xlim,ylim):
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.line1=None
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
    
        
    def draw(self,x,y,label):
        
        if self.line1 == None:
            self.line1, = self.ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma
 
        plt.title(label) 
        self.line1.set_data(x,y)
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
    
