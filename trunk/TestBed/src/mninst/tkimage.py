
import os, sys
import Tkinter
import Image, ImageTk
import gzip
import cPickle
from numpy import *
import PIL.Image

def grabImage(key):
    x=reshape(t[0][key],(28,28))
    x=x*256.0
    image=PIL.Image.fromarray(x)
    return image

def button_click_exit_mainloop (event):
    event.widget.quit() # this will cause mainloop to unblock.


data="mnist.pkl.gz"

f=gzip.open(data)

print " LOADING .....",
t,v,test=cPickle.load(f)    
print " DONE"


root = Tkinter.Tk()
root.bind("<Button>", button_click_exit_mainloop)
root.geometry('+%d+%d' % (100,100))

tkpi=[]
N=10
iw=28
ih=28
# root.geometry('%dx%d' % (iw*N,ih))

for i in range(N):
    image1 = grabImage(i)     # .open(f)
    tkpi.append(ImageTk.PhotoImage(image1))
    label_image = Tkinter.Label(root,image=tkpi[i])
    label_numb=Tkinter.Label(root,text=str(t[1][i]))
    label_image.grid(row=i,column=1)
    label_numb.grid(row=i,column=0)


root.title(f)
root.mainloop() # wait until user clicks the window
 