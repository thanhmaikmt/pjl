import gzip
import cPickle
import time
import os, sys
import Tkinter
import Image, ImageTk
import gzip
import cPickle
import numpy 
import PIL.Image
import tkMessageBox

def calc_dist(a,b):
    dist=0
    for i in range(len(a)):
        dist+=(a[i]-b[i])**2
    return dist

def calc_dist_numpy(a,b):
    c=a-b
    return (c*c).sum()


def grabImage(img):
    # print set[0][index]
    x=numpy.reshape(img,(28,28))
    x=x*256.0
    image=PIL.Image.fromarray(x)
    return image

tkimgs=[None,None]

def display(img1,lab1,img2,lab2):
    
    img1=grabImage(img1)
    img2=grabImage(img2)
    myrow=0
    tkimgs[0]=ImageTk.PhotoImage(img1)
    label_image1 = Tkinter.Label(frame,image=tkimgs[0])
    label_numb1=Tkinter.Label(frame,text=str(lab1))
    label_image1.grid(row=myrow,column=2)
    label_numb1.grid(row=myrow,column=1)
    
    tkimgs[1]=ImageTk.PhotoImage(img2)
    label_image2 = Tkinter.Label(frame,image=tkimgs[1])
    label_numb2=Tkinter.Label(frame,text=str(lab2))
    label_image2.grid(row=myrow,column=4)
    label_numb2.grid(row=myrow,column=3)
    frame.update()


def doit():    
        # compressed data 
    data="mnist_lite.pkl.gz"
    f=gzip.open(data)
    
    # load data into the 3 data sets
    print " LOADING .....  DATA . . . . . ",
    training_set,validation_set,test_set=cPickle.load(f)    
    print " DONE"
      
    nTrain=len(training_set[0])    # use first nTrain training examples
    nTest=len(test_set[0])     # test first nTest test cases 
    print "    Training set size: ",nTrain
    print "        Test set size: ",nTest
    
     
    
    countCorrect=0    #  counter for number of correct classifications
    
    
    #training_input=training_set[0]
    # using numpy arrays will speed things up by a few orders of magnitude
    training_input=numpy.array(training_set[0])
    
    #test_input=test_set[0]
    test_input=numpy.array(test_set[0])
    
    
    test_output=test_set[1]
    training_output=training_set[1] 
    
    # lets time this!! 
    start=time.time()
    
    
    BIG=1e32
 
    
    
    for i in range(nTest):    # for all test cases
        
        #  mindist and jNearest  keep track of best distance so far
        mindist = BIG
        jNearest =-1
    
        for j in range(nTrain):
            dist=calc_dist_numpy(training_input[j],test_input[i])
            if dist < mindist:
                mindist=dist
                jNearest=j
     
        print training_output[jNearest],test_output[i],mindist
            
        if  training_output[jNearest] == test_output[i]:
            countCorrect += 1
        else:
            display(training_input[jNearest],training_output[jNearest], 
                    test_input[i],test_output[i])
            time.sleep(1)
                
            
    end=time.time()
    
    print countCorrect," out of ",nTest, " In ",end-start," secs    ",  (countCorrect*100.0)/nTest, "%"

frame = Tkinter.Tk()


#frame=Tkinter.Frame(root)
#
b = Tkinter.Button(frame, text="RUN (RANDOM)", fg="black", command=doit)
b.grid(row=0,column=0)
frame.mainloop()


