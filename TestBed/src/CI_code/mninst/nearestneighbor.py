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
    
# compressed data 
data="mnist.pkl.gz"
f=gzip.open(data)

# load data into the 3 data sets
print " LOADING .....  DATA . . . . . ",
training_set,validation_set,test_set=cPickle.load(f)    
print " DONE"

print "    Training set size: ",len(training_set[0])
print "  Validation set size: ",len(validation_set[0])
print "        Test set size: ",len(test_set[0])

 

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

nTrain=50000    # use first nTrain training examples
nTest=10000      # test first nTest test cases


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
        
end=time.time()

print countCorrect," out of ",nTest, " In ",end-start," secs    ",  (countCorrect*100.0)/nTest, "%"
