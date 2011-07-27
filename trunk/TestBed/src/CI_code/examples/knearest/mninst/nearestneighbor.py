import gzip
import cPickle
import numpy
import time


def calc_dist(a,b):
    dist=0
    for i in range(len(a)):
        dist+=(a[i]-b[i])**2
    return dist

def calc_dist_numpy(a,b):
    c=a-b
    return (c*c).sum()


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
    
    
    
    # using numpy arrays will speed things up by a few orders of magnitude
    training_input=numpy.array(training_set[0])  
    test_input=numpy.array(test_set[0])
    
    # the outputs are parallel arrays
    test_output=test_set[1]
    training_output=training_set[1] 
    
    # lets time this!! 
    start=time.time()
    
    
    BIG=1e32
    

    countCorrect=0    #  counter for number of correct classifications
    countFail=0
    
    for i in range(nTest):    # for all test cases
        
        #  mindist and jNearest  keep track of best distance so far
        mindist = BIG
        jNearest =-1
    
        for j in range(nTrain):
            dist=calc_dist_numpy(training_input[j],test_input[i])
            if dist < mindist:
                mindist=dist
                jNearest=j
     
        # print training_output[jNearest],test_output[i],mindist
            
        if  training_output[jNearest] == test_output[i]:
            countCorrect += 1
        else:
            countFail += 1
            print i,":  " , (countCorrect*100.0)/(countCorrect+countFail), "%"
            
    end=time.time()
    
    print countCorrect," out of ",nTest, " In ",end-start," secs    ",  (countCorrect*100.0)/nTest, "%"


if __name__ == "__main__":
    doit()
