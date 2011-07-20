
import os, sys
import Tkinter
import Image, ImageTk
import gzip
import cPickle
from numpy import *
import PIL.Image

# get an image from the data set according to the given index

def grabImage(index,set):
    # print set[0][index]
    x=reshape(set[0][index],(28,28))
    x=x*256.0
    image=PIL.Image.fromarray(x)
    return image


#  exit application

def button_click_exit_mainloop (event):
    event.widget.quit() # this will cause mainloop to unblock.

# compressed data
data="mnist.pkl.gz"

f=gzip.open(data)

# load data into the 3 data sets
print " LOADING .....",
training_set,validation_set,test_set=cPickle.load(f)    
print " DONE"


# Root of the gui
root = Tkinter.Tk()


tkpimages=[]
N=10
iw=28
ih=28
# root.geometry('%dx%d' % (iw*N,ih))


set=validation_set

for i in range(N):
    image1 = grabImage(i,set)          
    # tkpimages.append(ImageTk.PhotoImage(image1))
    img=ImageTk.PhotoImage(image1)
    label_image = Tkinter.Label(root,image=img)  # tkpimages[i])
    label_numb=Tkinter.Label(root,text=str(set[1][i]))
    label_image.grid(row=i,column=1)
    label_numb.grid(row=i,column=0)


root.title(f)
root.mainloop() # wait until user clicks the window
 