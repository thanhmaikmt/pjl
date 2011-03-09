'''
Created on 4 Mar 2011

@author: pjl
'''
## {{{ http://code.activestate.com/recipes/521918/ (r3)
#!/usr/bin/env python

"""This is a small script to demonstrate using Tk to show PIL Image objects.
The advantage of this over using Image.show() is that it will reuse the
same window, so you can show multiple images without opening a new
window for each image.

This will simply go through each file in the current directory and
try to display it. If the file is not an image then it will be skipped.
Click on the image display window to go to the next image.

Noah Spurrier 2007
"""

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
root.geometry('%dx%d' % (iw*N,ih))

for i in range(N):
    image1 = grabImage(i)     # .open(f)
    tkpi.append(ImageTk.PhotoImage(image1))
    label_image = Tkinter.Label(root,image=tkpi[i])
    label_image.place(x=iw*i,y=0,width=iw,height=ih)


root.title(f)
root.mainloop() # wait until user clicks the window
 